
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("userprofile/<int:user_id>", views.userprofile, name="userprofile"),
    path("followuser/<int:user_id>", views.followuser, name="followuser"),
    path("following", views.following, name="following"),
    path("updatepost", views.updatepost, name="updatepost"),
    path("likepost/<int:post_id>", views.likepost, name="likepost")
]
