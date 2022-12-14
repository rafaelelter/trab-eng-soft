from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .forms import (
    SignupForm,
    OffererProfileForm,
    AddressForm,
    BuyerProfileForm,
    SearchOffererForm,
    CreateTicketForm,
    TicketPurchaseForm,
    TicketValidationForm,
)
from .models import OffererApproval, Profile, Ticket

import requests
import json
from datetime import datetime, timezone
import pytz

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

            user.save()
            
            address = address_form.save(commit=False)
            profile.address = address
            
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "street": f"{address.street_number} {address.street_name}",
                "format": "json",
                "limit": 1
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data:
                    address.latitude = data[0]["lat"]
                    address.longitude = data[0]["lon"]
                    address.save()
            else:
                address.save()

            profile.save()

            authenticated_user = authenticate(
                username=user_form.cleaned_data["username"],
                password=user_form.cleaned_data["password1"],
            )
            login(request, authenticated_user)

            messages.success(request, "Bem-vindo!")

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

        if all(
            (user_form.is_valid(), profile_form.is_valid())
            ):
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

            messages.success(request, "Bem-vindo!")

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


def is_approved_offerer_test(user):
    if user.is_authenticated and hasattr(user, "profile"):
        return user.profile.is_approved_offerer()
    return False


@user_passes_test(is_approved_offerer_test, login_url="/login")
def create_ticket(request):
    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.offerer = request.user.profile
            ticket.save()

            messages.success(request, "Ticket criado!")

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
            messages.success(request, "Ticket editado!")
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
    messages.success(request, "Ticket deletado!")
    return redirect("profile", pk=request.user.profile.pk)


def ticket_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    return render(request, "tickets/ticket.html", context={"ticket": ticket})

def is_buyer_test(user):
    if user.is_authenticated and hasattr(user, "profile"):
        return user.profile.is_buyer()
    return False

@user_passes_test(is_buyer_test, login_url="/login")
def purchase_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.buyer is not None:
        return redirect("tickets-home")
    
    if request.method == "POST":
        form = TicketPurchaseForm(request.POST, instance=ticket)
        if form.is_valid():
            expiration_date = form.cleaned_data["expiration_date"]
            expiration_time = form.cleaned_data["expiration_time"]
            if expiration_date is not None and expiration_time is not None:
                expiration = datetime.combine(expiration_date, expiration_time, tzinfo=pytz.timezone("America/Sao_Paulo"))
                expiration = expiration.replace(tzinfo=None)
            else:
                expiration = None


            ticket.buyer = request.user.profile
            ticket.expiration = expiration
            ticket.save()
            
            messages.success(request, "Ticket Comprado! N??mero de resgate: {}".format(ticket.random_id))

            return redirect("profile", pk=request.user.profile.pk)
    else:
        form = TicketPurchaseForm(instance=ticket)
    
    context = {"form": form}
    return render(request, "tickets/ticket_purchase.html", context)

def is_regulator_test(user):
    if user.is_authenticated and hasattr(user, "profile"):
        return user.profile.is_regulator()
    return False

@user_passes_test(is_regulator_test, login_url="/login")
def approve_offerer(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    approval = OffererApproval.objects.create(approved_offerer=profile.user, approved_by=request.user)
    approval.save()
    
    return redirect("profile", pk=profile.pk)

@user_passes_test(is_regulator_test, login_url="/login")
def delete_offerer(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    profile.delete()
    
    return redirect("tickets-home")

def validate_ticket(request):
    
    if request.method == "POST":
        form = TicketValidationForm(request.POST)
        if form.is_valid():
            random_id = form.cleaned_data["random_id"]
            password = form.cleaned_data["password"]
            ticket = get_object_or_404(Ticket, random_id=random_id, validated=False)

            if password == ticket.password:
                ticket.validated = True
                ticket.save()
                
                messages.success(request, "Ticket Validado!")
                
                return redirect("profile", pk=request.user.profile.pk)
            else:
                form.add_error("password", "Senha errada")
    else:
        form = TicketValidationForm()
        
    context = {"form": form}
    return render(request, "tickets/ticket_validation.html", context)

def search_offerer_map(request):
    profiles = Profile.objects.filter(user_type="O")

    js_marker_template = """
    var marker = L.marker([{latitude}, {longitude}]).addTo(map)
        .bindPopup('<b>{name}</b><br />{info}').openPopup();
    """

    coord_markers = []
    for profile in profiles:
        if profile.address.latitude and profile.address.longitude:
            coord_markers.append((
                profile.address.latitude,
                profile.address.longitude,
                profile.get_absolute_url(),
                profile.place_name,
            ))

    return render(request, "tickets/search_offerer_map.html", context={"my_list": json.dumps(coord_markers)})