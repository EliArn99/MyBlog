from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


@login_required
def home(request):
    return render(request, 'blog/home.html', {'user': request.user})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend when logging in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')  # Or the appropriate redirect
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})
