# urls.py
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('profile/', views.profile_view, name='profile'),  # Profile page URL
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('accounts/', include('allauth.urls')),  # Allauth URL маршрути
    path('register/', views.register_view, name='register'),
# urls.py
]
