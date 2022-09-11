from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from .forms import (
    SignupForm,
    OffererProfileForm,
    AddressForm,
    BuyerProfileForm,
    SearchOffererForm,
)
from .models import Profile


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