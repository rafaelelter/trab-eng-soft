from django.shortcuts import render
from django.contrib.auth.models import Group

from .forms import CreationForm


def index(request):
    return render(request, "tickets/index.html")


def signup(request):
    if request.method == "POST":
        form = CreationForm(request.POST)
        if form.is_valid():

            group_name = form.cleaned_data.get("group")
            user_group = Group.objects.get(name=group_name)

            user = form.save(user_group=user_group)

            return render(request, "tickets/index.html")
    else:
        form = CreationForm()
    return render(request, "registration/signup.html", {"form": form})
