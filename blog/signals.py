from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Post  # Your blog post model

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    # Create 'Author' group
    author_group, created = Group.objects.get_or_create(name='Author')

    # Assign permissions to Author (Add, Change, Delete Posts)
    content_type = ContentType.objects.get_for_model(Post)
    permissions = Permission.objects.filter(content_type=content_type)

    for permission in permissions:
        author_group.permissions.add(permission)

    # Create 'Reader' group (No special permissions)
    Group.objects.get_or_create(name='Reader')
