from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post, Category


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2'
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_picture']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
