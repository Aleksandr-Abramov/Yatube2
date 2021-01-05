from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Post
def index(request):
    posts = Post.objects.order_by("-pub_date")[:10]
    # posts = get_object_or_404(Post)
    context = {
        "posts": posts
    }
    return render(request, "index.html", context)
