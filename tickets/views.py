from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login


from .forms import CreationForm, OffererProfileForm


def index(request):
    return render(request, "tickets/index.html")


def signup(request):
    return render(request, "registration/signup.html")


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
            user_group = Group.objects.get(name="offerer")
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
