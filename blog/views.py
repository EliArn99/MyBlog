from django.shortcuts import render, get_object_or_404
# from .models import Post, Category
from django.contrib.auth.models import User

# Homepage View
def home(request):
    return render(request, 'blog/home.html', {'posts': posts})

# Post Detail Page
def post_detail(request, post_id):
    return render(request, 'blog/post_detail.html', {'post': post})

# About Page View
def about(request):
    return render(request, 'blog/about.html')

# Category Page View
def category_page(request, category_slug):
    return render(request, 'blog/category_page.html', {'category': category, 'posts': posts})

# User Profile Page View
def user_profile(request, username):
    return render(request, 'blog/user_profile.html', {'user': user, 'posts': posts})

# Contact Page View
def contact(request):
    return render(request, 'blog/contact.html')

# Privacy Policy Page View
def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')

# Terms of Service Page View
def terms_of_service(request):
    return render(request, 'blog/terms_of_service.html')
