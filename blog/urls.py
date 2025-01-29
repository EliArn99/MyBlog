# urls.py
from django.urls import path, include
from django.views.i18n import set_language

from . import views
urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('profile/', views.profile_view, name='profile'),  # Profile page URL
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('set-language/', set_language, name='set_language'),
    path('accounts/', include('allauth.urls')),  # Allauth URL маршрути
    path('register/', views.register_view, name='register'),
# urls.py
]
