from django.contrib import admin

from .models import Post, Group

# class PostAdmin(admin.ModelAdmin):
#     fields = ("text", "pub_date", "author")

admin.site.register(Post)
admin.site.register(Group)
