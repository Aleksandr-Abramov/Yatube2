from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Post, Group
from .forms import PostForm


def index(request):
    """Главная страница Index"""
    posts = Post.objects.order_by("-pub_date")[:10]
    # posts = get_object_or_404(Post)
    context = {
        "posts": posts
    }
    return render(request, "index.html", context)


def group_posts(request, slug):
    """Страница записей сообщества group_post"""
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    context = {
        "posts": posts,
        "group": group
    }
    return render(request, "group.html", context)


def new_post(request):
    """Страница оздание поста new"""
    if request.method != "POST":
        form = PostForm()
        context = {
            "form": form
        }
        return render(request, "new.html", context)

    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
