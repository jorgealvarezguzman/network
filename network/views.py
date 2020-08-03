from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import *

from .forms import NewPostForm


def index(request):
    posts = Post.objects.all()
    posts = [post for post in posts[::-1]]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def newpost(request):
    current_user = request.user
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["newpost"]
            Post.objects.create(user = current_user,
                                content = content)
    return redirect('index')


def userprofile(request, user_id):
    user = User.objects.get(id=user_id)
    current_user = request.user
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        current_user_profile, created = UserProfile.objects.get_or_create(user=current_user)
        number_of_followers = len(user_profile.followers.all())
        number_of_follows = len(user_profile.follows.all())
    except:
        number_of_followers = 0
        number_of_follows = 0
    posts = user.posts.all()
    posts = [post for post in posts[::-1]]
    # paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Check if current user is a follower of user
    is_follower = False
    if user_profile.followers.filter(pk=current_user.user_profile.id).exists():
        is_follower = True
    return render(request, "network/userprofile.html", {
        "number_of_followers": number_of_followers,
        "number_of_follows": number_of_follows,
        "page_obj": page_obj,
        "user": user,
        "current_user": current_user,
        "is_follower": is_follower
    })


def followuser(request, user_id):
    user = User.objects.get(id=user_id)
    current_user = request.user
    # get or create profiles
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    current_user_profile, created = UserProfile.objects.get_or_create(user=current_user)
    # check if current user is follower of user
    is_follower = user_profile.followers.filter(pk=current_user_profile.id).exists()
    if is_follower:
        # unfollow user
        user_profile.followers.remove(current_user_profile)
        return redirect('userprofile', user_id)
    # follow user
    user_profile.followers.add(current_user_profile)
    return redirect('userprofile', user_id)


@login_required
def following(request):
    current_user = request.user
    follows = current_user.user_profile.follows.all()
    # Create list with posts of all users that is following
    posts = [post for user_profile in follows
            for post in user_profile.user.posts.all()]
    posts.sort(key=lambda post: post.date_added)
    posts = [post for post in posts[::-1]]
    # paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html",{
        "page_obj": page_obj
    })
