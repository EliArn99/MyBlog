# urls.py
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),  # Home page

    path('accounts/', include('allauth.urls')),  # Allauth URL маршрути
    path('register/', views.register_view, name='register'),
# urls.py
]
