from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Message

@login_required
def index(request):
    latest_messages_list = Message.objects.order_by("-time")
    context = {"latest_messages_list": latest_messages_list}
    return render(request, "chat/index.html", context)


def sign_up(request):
    return render(request, "chat/sign-up.html")


def info(request):
    return render(request, "chat/info.html")


def sign_in(request):
    return render(request, "chat/sign-in.html")

@login_required
def members(request):
    return render(request, "chat/members.html")