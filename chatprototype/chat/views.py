from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.views.decorators.cache import cache_page

from django.views.decorators.csrf import csrf_protect

from .models import Message
from .time_measurement import measure_time


@login_required
@measure_time
@cache_page(60)
def index(request):
    if request.method == "GET":
        return view_messages(request)

    if request.method == "POST":
        return send_message(request)


def view_messages(request):
    latest_messages_list = get_messages()
    context = {"latest_messages_list": latest_messages_list, "is_user_authenticated": request.user.is_authenticated}
    return render(request, "chat/index.html", context)


def get_messages():
    messages = Message.objects.order_by("time")
    return messages


def send_message(request):
    message_text = request.POST.get("text")
    message = Message.objects.create(text=message_text, time=datetime.now(), user=request.user)
    message.save()
    return redirect("/")


def sign_up(request):
    if request.method == "GET":
        return render(request, "chat/sign-up.html")

    if request.method == "POST":
        return login_user(request)


def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    repeat_password = request.POST.get('repeat_password')
    email = request.POST.get("email")

    print(username)
    print(password)
    print(email)

    if password != repeat_password:
        return redirect("sign-up/")

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()

    login(request, user)
    return redirect("/")


def info(request):
    return render(request, "chat/info.html")


def sign_in(request):
    if request.method == "POST":
        return make_login(request)

    return render(request, "chat/sign-in.html")


def make_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)

    print(user)
    if user is not None:
        login(request, user)

    return redirect("/")


@login_required
@measure_time
@cache_page(60)
def members(request):
    members_list = get_members()
    context = {"members_list": members_list}
    return render(request, "chat/members.html", context)


def get_members():
    members_list = set(map(lambda message: message.user, Message.objects.all()))
    return members_list


@login_required
def make_logout(request):
    if request.method == "POST" and request.user.is_authenticated:
            logout(request)
    return redirect("/")