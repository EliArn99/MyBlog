from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProfileForm, ProfileEditForm
from django.contrib.auth.models import Permission


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
