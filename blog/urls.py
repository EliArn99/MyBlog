# urls.py
from django.urls import path, include
from django.views.i18n import set_language
from django.contrib.auth import views as auth_views
from . import views
from .views import signup_view, dashboard_view

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
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('accounts/', include('allauth.urls')),  # Allauth URL маршрути
    path('register/', views.register_view, name='register'),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Signup
    path("signup/", signup_view, name="signup"),

    path('reader-dashboard/', views.reader_dashboard_view, name='reader_dashboard'),

    # Define other necessary URL patterns
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('author-dashboard/', views.author_dashboard_view, name='author_dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # urls.py
]
