from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home_view(request):
    return render(request, 'home.html')



def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return render(request,'success.html')  # aage banayenge
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')  # ✅ this works!
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


from .models import Post, UserProfile

def post_list_view(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'posts': posts})
    else:
        return render(request, 'home.html')

# social/views.py

from .models import Comment
from django.contrib.auth.decorators import login_required
@login_required
def post_detail_view(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(post=post, user=request.user, content=content)
        return redirect('post_detail', post_id=post_id)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments
    })

from .models import Like
from django.shortcuts import get_object_or_404

@login_required
def like_post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # Unlike
    return redirect('post_list')  # ya 'post_detail', post_id=post.id


def profile_view(request, username):
    user_obj = User.objects.get(username=username)
    profile, _ = UserProfile.objects.get_or_create(user=user_obj)
    posts = Post.objects.filter(user=user_obj).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated and request.user != user_obj:
        is_following = Follow.objects.filter(follower=request.user, following=user_obj).exists()

    return render(request, 'profile.html', {
        'profile_user': user_obj,
        'profile': profile,
        'posts': posts,
        'is_following': is_following
    })


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
from .forms import ProfileUpdateForm


@login_required
def profile_update_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile_update.html', {'form': form})

from .models import Follow

@login_required
def toggle_follow_view(request, username):
    target_user = User.objects.get(username=username)
    
    if request.user == target_user:
        return redirect('profile', username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        follow.delete()  # Unfollow

    return redirect('profile', username=username)



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post

@login_required
def global_feed_view(request):
    posts = Post.objects.all().order_by('-created_at')  # Sabhi posts
    return render(request, 'global_feed.html', {'posts': posts})


from django.contrib.auth.models import User
from django.shortcuts import render

def search_users_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = User.objects.filter(username__icontains=query)

    return render(request, 'search_results.html', {'results': results, 'query': query})


from .forms import PostForm
from django.contrib.auth.decorators import login_required

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')  # ya 'feed' agar wo default page hai
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})



# social/views.py

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'delete_post.html', {'post': post})

from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(to_user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


# social/views.py

from .models import SavedPost

@login_required
def toggle_save_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        saved.delete()
    return redirect('post_detail', post_id=post.id)

@login_required
def saved_posts_view(request):
    saved = SavedPost.objects.filter(user=request.user).select_related('post').order_by('-saved_at')
    posts = [item.post for item in saved]
    return render(request, 'saved_posts.html', {'posts': posts})


def success_view(request):
    return render(request,"success.html")

def main_view(request):
    return render(request,"main.html")

def github_demo(request):
    return render(request, 'login.html')  # or just HttpResponse("GitHub login demo")

def LinkedIn_demo(request):
    return render(request, 'login.html')
