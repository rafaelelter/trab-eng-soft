from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test

from .forms import (
    SignupForm,
    OffererProfileForm,
    AddressForm,
    BuyerProfileForm,
    SearchOffererForm,
    CreateTicketForm,
)
from .models import Profile, Ticket


def home(request):
    return render(request, "tickets/home.html")


def signup(request):
    return render(request, "tickets/signup.html")


def signup_offerer(request):
    if request.method == "POST":
        user_form = SignupForm(request.POST)
        profile_form = OffererProfileForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST)
        if all(
            (user_form.is_valid(), profile_form.is_valid(), address_form.is_valid())
        ):
            user = user_form.save(commit=False)
            user.first_name = user_form.cleaned_data["first_name"]
            user.last_name = user_form.cleaned_data["last_name"]
            user.email = user_form.cleaned_data["email"]

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.user_type = "O"

            address = address_form.save(commit=False)
            profile.address = address

            user.save()
            profile.save()
            address.save()

            authenticated_user = authenticate(
                username=user_form.cleaned_data["username"],
                password=user_form.cleaned_data["password1"],
            )
            login(request, authenticated_user)

            return redirect("tickets-home")
    else:
        user_form = SignupForm()
        profile_form = OffererProfileForm()
        address_form = AddressForm()
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "address_form": address_form,
    }
    return render(request, "tickets/signup_offerer.html", context)


def signup_buyer(request):
    if request.method == "POST":
        user_form = SignupForm(request.POST)
        profile_form = BuyerProfileForm(request.POST, request.FILES)

        if all(user_form.is_valid(), profile_form.is_valid()):
            user = user_form.save(commit=False)
            user.first_name = user_form.cleaned_data["first_name"]
            user.last_name = user_form.cleaned_data["last_name"]
            user.email = user_form.cleaned_data["email"]

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.user_type = "B"

            user.save()
            profile.save()

            user = authenticate(
                username=user_form.cleaned_data["username"],
                password=user_form.cleaned_data["password1"],
            )
            login(request, user)
            return redirect("tickets-home")
    else:
        user_form = SignupForm()
        profile_form = BuyerProfileForm()
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "tickets/signup_buyer.html", context)


def search_offerer(request):
    if request.method == "POST":
        form = SearchOffererForm(request.POST)

        if form.is_valid():
            offerers = Profile.objects.filter(
                user_type="O",
                place_name__icontains=form.cleaned_data["search"],
            )
            context = {"offerers": offerers}
            return render(request, "tickets/search_offerer.html", context)
    else:
        form = SearchOffererForm()
    context = {"form": form}
    return render(request, "tickets/search_offerer.html", context)


def profile_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    return render(request, "tickets/profile.html", context={"profile": profile})


def is_offerer_test(user):
    if user.is_authenticated and hasattr(user, "profile"):
        return user.profile.is_offerer()
    return False


@user_passes_test(is_offerer_test, login_url="/login")
def create_ticket(request):
    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.offerer = request.user.profile
            ticket.save()
            return redirect("tickets-home")
    else:
        form = CreateTicketForm()
    context = {"form": form}
    return render(request, "tickets/ticket_creation.html", context)


def is_offerers_ticket(user, ticket):
    if user.is_authenticated and hasattr(user, "profile"):
        return user.profile == ticket.offerer
    return False


def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.offerer != request.user.profile:
        return redirect("tickets-home")

    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=request.user.profile.pk)
    else:
        form = CreateTicketForm(instance=ticket)
    context = {"form": form}
    return render(request, "tickets/ticket_creation.html", context)


def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.offerer != request.user.profile:
        return redirect("tickets-home")
    ticket.set_picture_default()
    ticket.delete()
    return redirect("profile", pk=request.user.profile.pk)


def ticket_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    return render(request, "tickets/ticket.html", context={"ticket": ticket})
