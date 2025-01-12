# In your app's urls.py

from django.urls import path
from . import views  # Import your views here

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),  # Services page
    path('category/book-reviews/', views.book_reviews, name='book_reviews'),  # Book Reviews page
    path('category/lifestyle/', views.lifestyle, name='lifestyle'),  # Lifestyle page
    path('category/technology/', views.technology, name='technology'),  # Technology page
    path('category/education/', views.education, name='education'),  # Education & Learning page
    path('category/environment/', views.environment, name='environment'),  # Environment & Nature page
    path('category/art-and-culture/', views.art_and_culture, name='art_and_culture'),  # Art & Culture page
    path('category/gaming/', views.gaming, name='gaming'),  # Gaming page
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Privacy Policy page
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register, name='register'),
]
