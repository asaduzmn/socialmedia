from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm, PostForm
from .models import Post

def home(request):
    # Get query parameters
    query = request.GET.get('q')  # Search keyword
    user_filter = request.GET.get('user_filter')  # Filter by user
    media_type = request.GET.get('media_type', 'all')  # Filter by media type
    sort_by = request.GET.get('sort_by', 'newest')  # Sort by date

    # Start with all posts
    posts = Post.objects.all()

    # Keyword search
    if query:
        posts = posts.filter(Q(content__icontains=query))

    # Filter by user
    if user_filter:
        posts = posts.filter(user__username=user_filter)

    # Filter by media type
    if media_type == 'text':
        posts = posts.filter(image__isnull=True)  # Text-only posts (no image)
    elif media_type == 'image':
        posts = posts.filter(image__isnull=False)  # Posts with images
    elif media_type == 'image_only':
        posts = posts.filter(image__isnull=False, content__isnull=True)  # Image-only posts (no text)

    # Sort by date
    if sort_by == 'oldest':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'core/home.html', {'posts': posts})

@login_required
def profile(request):
    # Get query parameters
    query = request.GET.get('q')  # Search keyword
    media_type = request.GET.get('media_type', 'all')  # Filter by media type
    sort_by = request.GET.get('sort_by', 'newest')  # Sort by date

    # Start with the logged-in user's posts
    posts = Post.objects.filter(user=request.user)

    # Keyword search
    if query:
        posts = posts.filter(Q(content__icontains=query))

    # Filter by media type
    if media_type == 'text':
        posts = posts.filter(image__isnull=True)  # Text-only posts (no image)
    elif media_type == 'image':
        posts = posts.filter(image__isnull=False)  # Posts with images
    elif media_type == 'image_only':
        posts = posts.filter(image__isnull=False, content__isnull=True)  # Image-only posts (no text)

    # Sort by date
    if sort_by == 'oldest':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'core/profile.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'core/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    return redirect('profile')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

