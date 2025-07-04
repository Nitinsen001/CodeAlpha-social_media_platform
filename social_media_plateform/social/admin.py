
# Register your models here.
from django.contrib import admin
from .models import UserProfile, Post, Comment, Like, Follow

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
