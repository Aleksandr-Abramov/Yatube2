from django.contrib import admin

from .models import Post

# class PostAdmin(admin.ModelAdmin):
#     fields = ("text", "pub_date", "author")

admin.site.register(Post)
