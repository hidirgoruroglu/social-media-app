from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost,FollowersCount
from itertools import chain
import random
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username = request.user.username)
        user_profile = Profile.objects.get(user = user_object)
        user_following_list = []
        feed = []

        user_following = FollowersCount.objects.filter(follower=request.user.username)
        for users in user_following:
            user_following_list.append(users.user)
        
        for usernames in user_following_list:
            feed_list = Post.objects.filter(user = usernames)
            feed.append(feed_list)
        feed_list = list(chain(*feed))
        # posts = Post.objects.all()
        
        all_users = User.objects.all()
        user_following_all = []

        for user in user_following:
            user_list = User.objects.get(username = user.user)
            user_following_all.append(user_list)
        
        new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
        current_user = User.objects.filter(username=request.user.username)
        final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
        random.shuffle(final_suggestions_list)


        username_profile = []
        username_profile_list = []
        for users in final_suggestions_list:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        suggestions_username_profile_list = list(chain(*username_profile_list))
        context = dict(user_profile = user_profile,posts = feed_list, suggestions_username_profile_list = suggestions_username_profile_list[:4])
    else:
        return redirect("account_login")

    
    return render(request,"index.html",context)

@login_required(login_url="account_login")
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get("image_upload")
        caption = request.POST.get("caption")
        new_post = Post.objects.create(user= user,image = image,caption = caption)
        new_post.save()
        return redirect("index")
    else:
        return redirect("index")

@login_required(login_url="account_login")
def settings(request):
    user_profile = Profile.objects.get(user = request.user)
    if request.method == "POST":
        if request.FILES.get("image") == None:
            image = user_profile.profile_img
            bio = request.POST.get("bio")
            location = request.POST.get("location")

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        if request.FILES.get("image") != None:
            image = request.FILES.get("image")
            bio = request.POST.get("bio")
            location = request.POST.get("location")

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect("settings")

    context = dict(user_profile = user_profile)
    return render(request,"settings.html",context)

@login_required(login_url="account_login")
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes +=1
        post.save()
        return redirect("index")
    else:
        like_filter.delete()
        post.no_of_likes -=1
        post.save()
        return redirect("index")

@login_required(login_url="account_login")
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user = pk)
    user_posts_length = len(user_posts)
    follower = request.user.username
    user = pk
    if FollowersCount.objects.filter(follower = follower,user = user).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"
    user_followers = len(FollowersCount.objects.filter(user = pk))
    user_following = len(FollowersCount.objects.filter(follower = pk))

    context = dict(user_object = user_object,
                   user_profile = user_profile,
                   user_posts = user_posts,
                   user_posts_length = user_posts_length,
                   button_text = button_text,
                   user_followers = user_followers,
                   user_following = user_following,
                   )
    
    return render(request,"profile.html",context)

@login_required(login_url="account_login")
def follow(request):
    if request.method == "POST":
        follower = request.POST.get("follower")
        user = request.POST.get("user")
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect("/profile/"+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect("/profile/"+user)
    else:
        return redirect("index")

@login_required(login_url="account_login")
def search(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    if request.method == "POST":
        username = request.POST.get("username")
        username_object = User.objects.filter(username__icontains = username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user = ids) 
            username_profile_list.append(profile_lists)
        username_profile_list = list(chain(*username_profile_list))
    context = dict(user_profile = user_profile,username_profile_list = username_profile_list)
    return render(request,"search.html",context)