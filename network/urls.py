
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API paths
    path("alllikes", views.alllikes, name="alllikes"),
    path("alllikes/<int:id>", views.likeid, name="likeid"),
    path("follows", views.follows, name="follows"),
    path("follows/<int:id>", views.followid, name="followid"),
    path("postsapi", views.postsapi, name="postsapi"),
    path("postsapi/<int:id>", views.postsapiid, name="postsapiid")    
]
