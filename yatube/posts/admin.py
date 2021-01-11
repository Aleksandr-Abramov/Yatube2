from django.contrib import admin

from .models import Post, Group, Comment

# class PostAdmin(admin.ModelAdmin):
#     fields = ("text", "pub_date", "author")

admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Comment)