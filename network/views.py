from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.core.paginator import Paginator, EmptyPage

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by('-time')
    activePosts = {}
    isLiked = {}
    likeIds = {}
    for post in posts:
        isLiked[post] = False
        if request.user.is_authenticated:
            # If user has liked this post in the past
            if Like.objects.filter(postId=post.id, liker=request.user).count() > 0:
                currentLike = Like.objects.get(postId=post.id, liker=request.user)
                likeIds[post.id] = currentLike.id
            if Like.objects.filter(postId=post.id, liker=request.user, is_liked=True).count() > 0:
                isLiked[post] = True
        count = Like.objects.filter(postId=post.id, is_liked=True).count()
        activePosts[post] = count
        p = Paginator(posts, 10)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
    return render(request, "network/index.html", {"activePosts": activePosts, "page": page, "isLiked": isLiked, "likeIds": likeIds})


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

@login_required
def newpost(request):
    if request.method == "POST":
        post = Post(poster=request.user, content=request.POST["content"])
        post.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(poster=user.id).order_by('-time')
    activePosts = {}
    isLiked = {}
    likeIds = {}
    followIds = {}
    followsAccount = False
    if request.user.is_authenticated:
        # Filter all follow objects by current user
        userFollows = Follow.objects.filter(follower=request.user)
        # Calculate if current user follows this profile
        followObject = Follow.objects.filter(follower=request.user, account=user).first()
        if followObject and followObject.is_following == True:
            followsAccount = True
        for follow in userFollows:
            # Retrieve follow IDs for all accounts current user is following
            followIds[follow.account] = follow.id
    # Calculate the current follower count for this profile
    followers = Follow.objects.filter(account=user, is_following=True).count()
    # Calculate the current number of accounts this profile is following
    followingCount = 0
    if Follow.objects.filter(follower=user, is_following=True).count() > 0:
        followingCount = Follow.objects.filter(follower=user).count()
    for post in posts:
        isLiked[post] = False
        if request.user.is_authenticated:
            # If user has liked this post in the past
            if Like.objects.filter(postId=post.id, liker=request.user).count() > 0:
                currentLike = Like.objects.get(postId=post.id, liker=request.user)
                likeIds[post.id] = currentLike.id
            if Like.objects.filter(postId=post.id, liker=request.user, is_liked=True).count() > 0:
                isLiked[post] = True
        count = Like.objects.filter(postId=post.id, is_liked=True).count()
        activePosts[post] = count
    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return render(request, "network/profile.html", {
        "activePosts": activePosts,
        "page": page, 
        "isLiked": isLiked, 
        "likeIds": likeIds,
        "followIds": followIds, 
        "followers": followers,
        "followsAccount": followsAccount,
        "followingCount": followingCount,
        "profile": user,
        "currentUser": request.user
        })


# Function for the /following path
@login_required
def following(request):
    followings = Follow.objects.filter(follower=request.user, is_following=True)
    followedAccounts = []
    for following in followings:
        followedAccounts.append(following.account)
    posts = Post.objects.filter(poster__in=followedAccounts).order_by('-time')
    activePosts = {}
    isLiked = {}
    likeIds = {}
    for post in posts:
        isLiked[post] = False
        # If user has liked this post in the past
        if Like.objects.filter(postId=post.id, liker=request.user).count() > 0:
            currentLike = Like.objects.get(postId=post.id, liker=request.user)
            likeIds[post.id] = currentLike.id
        if Like.objects.filter(postId=post.id, liker=request.user, is_liked=True).count() > 0:
            isLiked[post] = True
        count = Like.objects.filter(postId=post.id, is_liked=True).count()
        activePosts[post] = count
    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return render(request, "network/following.html", {"activePosts": activePosts, "page": page, "isLiked": isLiked, "likeIds": likeIds})


# API views

@csrf_exempt
@login_required
def alllikes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        newLike = Like(liker=request.user, postId=data.get("postId"))
        newLike.save()
        likes = Like.objects.all()
        return JsonResponse([like.serialize() for like in likes], safe=False)

    if request.method == "GET":
        likes = Like.objects.all()
        if request.user.is_superuser:
            return JsonResponse([like.serialize() for like in likes], safe=False)
        else:
            return JsonResponse({
                "error": "This account is not authorized to view this API."
            }, status=400)

@csrf_exempt
@login_required
def likeid(request, id):

    # Query for requested like
    try:
        like = Like.objects.get(id=id)
    except Like.DoesNotExist:
        return JsonResponse({"error": "Like not found."}, status=404)

    # Return like contents
    if request.method == "GET":
        if request.user.is_superuser:
            return JsonResponse(like.serialize())
        else:
            return JsonResponse({
                "error": "This account is not authorized to view this API."
            }, status=400)

    # Update like if unliked
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("is_liked") is not None:
            like.is_liked = data["is_liked"]
        like.save()
        return HttpResponse(status=204)

    # Like must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    
@csrf_exempt
@login_required
def follows(request):
    if request.method == "POST":
        data = json.loads(request.body)
        accountUser = User.objects.get(username=data.get("account"))
        newFollow = Follow(follower=request.user, account=accountUser)
        newFollow.save()
        follows = Follow.objects.all()
        return JsonResponse([follow.serialize() for follow in follows], safe=False)

    if request.method == "GET":
        follows = Follow.objects.all()
        if request.user.is_superuser:
            return JsonResponse([follow.serialize() for follow in follows], safe=False)
        else:
            return JsonResponse({
                "error": "This account is not authorized to view this API."
            }, status=400)

@csrf_exempt
@login_required
def followid(request, id):

    # Query for requested follow
    try:
        follow = Follow.objects.get(id=id)
    except Follow.DoesNotExist:
        return JsonResponse({"error": "Follow not found."}, status=404)

    # Return follow contents
    if request.method == "GET":
        if request.user.is_superuser:
            return JsonResponse(follow.serialize())
        else:
            return JsonResponse({
                "error": "This account is not authorized to view this API."
            }, status=400)

    # Update follow object if unfollowed
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("is_following") is not None:
            follow.is_following = data["is_following"]
        follow.save()
        return HttpResponse(status=204)

    # Follow must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def postsapi(request):
    if request.method == "GET":
        posts = Post.objects.all()
        if request.user.is_superuser:
            return JsonResponse([post.serialize() for post in posts], safe=False)
        else:
            return JsonResponse({
                "error": "This account is not authorized to view this API."
            }, status=400)
    # Postsapi must be via GET
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

@csrf_exempt
@login_required
def postsapiid(request, id):
    # Query for requested post
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        if request.user.is_superuser:
            return JsonResponse(post.serialize())
        else:
            return JsonResponse({
                "error": "This account is not authorized to view this API."
            }, status=400)

    # Update post content if PUT request
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

