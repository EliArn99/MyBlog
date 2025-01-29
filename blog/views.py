from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProfileForm, ProfileEditForm
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from .models import Post, Category
from .forms import PostForm, CategoryForm
from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import gettext as _
from .models import Post

def assign_permissions_based_on_role(user):
    if user.role == 'admin':
        permissions = Permission.objects.all()  # Admin gets all permissions
    elif user.role == 'author':
        permissions = Permission.objects.filter(codename='can_create_content')  # Authors can create content
    elif user.role == 'reader':
        permissions = Permission.objects.filter(codename='can_read_content')  # Readers can only read content

    user.user_permissions.set(permissions)  # Assign the permissions to the user
    user.save()


@login_required
def change_user_role(request, user_id):
    if request.user.role != 'admin':
        return redirect('home')  # Ensure only admins can access this view

    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role')
        user.role = new_role
        user.save()
        return redirect('admin_dashboard')  # Redirect to an admin dashboard or users list page

    return render(request, 'blog/change_user_role.html', {'user': user})


# Use this in your registration view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            assign_permissions_based_on_role(user)  # Assign permissions based on role
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')  # Redirect to the homepage or a dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def author_required(function):
    return user_passes_test(lambda u: u.role == 'author', login_url='home')(function)


@login_required
@author_required
def create_content_view(request):
    # Only accessible by authors
    return render(request, 'blog/create_content.html')


def reader_required(function):
    return user_passes_test(lambda u: u.role == 'reader', login_url='home')(function)


@login_required
@reader_required
def read_content_view(request):
    # Only accessible by readers
    return render(request, 'blog/read_content.html')


@login_required
def home(request):
    return render(request, 'blog/home.html', {'user': request.user})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same profile page or another page
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})


@login_required
def profile_edit_view(request):
    """View to edit the user profile."""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'blog/profile_edit.html', {'form': form})







def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(status='published')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |  # Search in title
            Q(categories__name__icontains=query) |  # Search in categories
            Q(tags__name__icontains=query)  # Search in tags
        ).distinct()

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'query': query,
    })

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the logged-in user as the author
            post.status = 'published'  # Ensure the post is published immediately
            post.save()
            form.save_m2m()  # Save tags
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)  # Remove from dislikes if already disliked
    post.likes.add(request.user)  # Add the like
    return redirect('post_detail', post_id=post.id)


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Remove from likes if already liked
    post.dislikes.add(request.user)  # Add the dislike
    return redirect('post_detail', post_id=post.id)


