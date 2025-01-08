from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_slug>/', views.category_page, name='category_page'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]
