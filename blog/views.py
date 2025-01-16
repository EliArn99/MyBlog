# Homepage View
from django.shortcuts import render, redirect
from django.contrib import messages

from MyBlog.blog.forms import CustomUserCreationForm


def home(request):
    return render(request, 'blog/home.html')

# Post Detail Page
def post_detail(request, post_id):
    return render(request, 'blog/post_detail.html')

# About Page View
def about(request):
    return render(request, 'blog/about.html')

# Category Page View
def category_page(request, category_slug):
    return render(request, 'blog/category_page.html')

# User Profile Page View
def user_profile(request, username):
    return render(request, 'blog/user_profile.html')

# Contact Page View
def contact(request):
    return render(request, 'blog/contact.html')

# Privacy Policy Page View
def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')

# Terms of Service Page View
def terms_of_service(request):
    return render(request, 'blog/terms_of_service.html')


def book_reviews(request):
    return render(request, 'category/book_reviews.html')

def lifestyle(request):
    return render(request, 'category/lifestyle.html')

def technology(request):
    return render(request, 'category/technology.html')

def education(request):
    return render(request, 'category/education.html')

def environment(request):
    return render(request, 'category/environment.html')

def art_and_culture(request):
    return render(request, 'category/art_and_culture.html')

def gaming(request):
    return render(request, 'category/gaming.html')



def login_view(request):
    return render(request, 'blog/login.html' )



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully! You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})
