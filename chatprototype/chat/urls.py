from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("sign-in/", views.sign_in, name="sign-in"),
    path("info/", views.info, name="info"),
    path("members/", views.members, name='members'),
    path("logout/", views.make_logout, name="logout"),
]