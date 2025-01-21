# Homepage View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from MyBlog.blog.forms import CustomUserCreationForm, BookReviewForm
from MyBlog.blog.models import Book


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
    books = Book.objects.all()
    for book in books:
        if not book.cover_image:
            book.cover_image = 'book_covers/default_cover.jpg'  # Assign a default path
    return render(request, 'category/book_reviews.html', {'books': books})


@login_required
def add_review(request):
    if request.method == 'POST':
        form = BookReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_reviews')
    else:
        form = BookReviewForm()
    return render(request, 'category/add_review.html', {'form': form})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'category/book_detail.html', {'book': book})

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
