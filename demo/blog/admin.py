from django.contrib import admin
from . models import Category, Comment, Dislike, Favourite, Like, Post, Profile

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Favourite)
admin.site.register(Like)
admin.site.register(Dislike)