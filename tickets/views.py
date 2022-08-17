from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test

from .models import OffererProfile, Ticket
from .forms import (
    CreationForm,
    OffererProfileForm,
    OffererSearchForm,
    TicketCreationForm,
)


def index(request):
    return render(request, "tickets/index.html")


def signup(request):
    return render(request, "registration/signup.html")


def search(request):
    if request.method == "POST":
        form = OffererSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            offerers = OffererProfile.objects.filter(user__username__icontains=search)
    else:
        offerers = None
    form = OffererSearchForm()
    return render(request, "tickets/search.html", {"form": form, "offerers": offerers})


def offerer_detail(request, pk):
    offerer = get_object_or_404(OffererProfile, pk=pk)
    return render(request, "tickets/offerer-detail.html", {"offerer": offerer})

def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, "tickets/ticket-detail.html", {"ticket": ticket})

def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.offerer.user == request.user:
        ticket.delete()
    return render(request, "tickets/index.html")

def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = TicketCreationForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.offerer = request.user.offererprofile
            ticket.save()
            return render(request, "tickets/index.html")
    else:
        form = TicketCreationForm(instance=ticket)
    return render(request, "tickets/new-ticket.html", {"form": form})

def exchange_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.validated = True
    ticket.save()
    return render(request, "tickets/index.html")

def new_ticket(request):
    if request.method == "POST":
        form = TicketCreationForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.offerer = request.user.offererprofile
            ticket.save()
            return render(request, "tickets/index.html")
    else:
        form = TicketCreationForm()
    return render(request, "tickets/new-ticket.html", {"form": form})

@user_passes_test(lambda u: u.groups.filter(name="regulator").exists())
def approve_offerer(request, pk):
    offerer = get_object_or_404(OffererProfile, pk=pk)
    offerer.user.groups.remove(Group.objects.get(name="unapproved_offerer"))
    offerer.user.groups.add(Group.objects.get(name="offerer"))
    offerer.is_approved = True
    offerer.save()
    return render(request, "tickets/index.html")

def signup_buyer(request):
    if request.method == "POST":
        form = CreationForm(request.POST)
        if form.is_valid():
            user_group = Group.objects.get(name="buyer")
            user = form.save(user_group=user_group)

            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)

            return render(request, "tickets/index.html")
    else:
        form = CreationForm()
    return render(request, "registration/signup-buyer.html", {"form": form})


def signup_offerer(request):
    if request.method == "POST":
        u_form = CreationForm(request.POST)
        p_form = OffererProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user_group = Group.objects.get(name="unapproved_offerer")
            user = u_form.save(user_group=user_group)
            profile = p_form.save(user=user)

            new_user = authenticate(
                username=u_form.cleaned_data["username"],
                password=u_form.cleaned_data["password1"],
            )
            login(request, new_user)

            return render(request, "tickets/index.html")
    else:
        u_form = CreationForm()
        p_form = OffererProfileForm()
    return render(
        request,
        "registration/signup-offerer.html",
        {"u_form": u_form, "p_form": p_form},
    )
