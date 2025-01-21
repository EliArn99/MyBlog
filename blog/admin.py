from django.contrib import admin
from .models import CustomUser, Category, Post, Comment, Tag, PostTag, ContactMessage, PrivacyPolicy, TermsOfService, PostLike, UserFollow

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(PostTag)
admin.site.register(ContactMessage)
admin.site.register(PrivacyPolicy)
admin.site.register(TermsOfService)
admin.site.register(PostLike)
admin.site.register(UserFollow)
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')
