from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm, ProfileForm, ProfileEditForm, CommentForm
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db.models import Q
from .models import Post
from django.core.paginator import Paginator
from .forms import SignupForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def assign_permissions_based_on_role(user):
    if user.role == 'admin':
        permissions = Permission.objects.all()
    elif user.role == 'author':
        permissions = Permission.objects.filter(codename='can_create_content')
    elif user.role == 'reader':
        permissions = Permission.objects.filter(codename='can_read_content')

    user.user_permissions.set(permissions)
    user.save()


@login_required
def change_user_role(request, user_id):
    if request.user.role != 'admin':
        return redirect('home')

    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role')
        user.role = new_role
        user.save()
        return redirect('admin_dashboard')

    return render(request, 'blog/change_user_role.html', {'user': user})


# Use this in your registration view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            assign_permissions_based_on_role(user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect("home")  # Redirect to home page
    else:
        form = SignupForm()
    return render(request, "blog/login.html", {"form": form})


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
            return redirect('profile')
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
            Q(title__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    # Pagination: 10 posts per page
    paginator = Paginator(posts, 9)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})


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
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
    })


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    post.likes.add(request.user)  # Add the like
    return redirect('post_detail', post_id=post.id)


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    post.dislikes.add(request.user)
    return redirect('post_detail', post_id=post.id)


def custom_404(request, exception):
    return render(request, 'blog/404.html', status=404)


@login_required
def dashboard_view(request):
    if request.user.role == "admin":
        return redirect("admin_dashboard")
    elif request.user.role == "author":
        return render(request, 'dashboard/author_dashboard.html')
    elif request.user.role == "reader":
        return render(request, 'dashboard/reader_dashboard.html')  # Use the namespace here if applicable
    return redirect("home")




# Define the reader dashboard view
def reader_dashboard_view(request):
    return render(request, 'blog/reader_dashboard.html')  # Adjust the template path as necessary

def admin_dashboard_view(request):
    pass

def author_dashboard_view(request):
    pass


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "blog/login.html", {"form": form})
