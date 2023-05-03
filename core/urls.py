from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("accounts/settings",views.settings,name="settings"),
    path("upload/",views.upload,name="upload"),
    path("search/",views.search,name="search"),
    path("follow/",views.follow,name="follow"),
    path("like-post/",views.like_post,name="like-post"),
    path("profile/<str:pk>", views.profile, name='profile'),
]
