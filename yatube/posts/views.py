from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm


def index(request):
    """Главная страница Index"""
    # posts = Post.objects.order_by("-pub_date")[:10]
    # posts = get_object_or_404(Post)
    post_list = Post.objects.select_related("group")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page
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

# @login_required
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


def profile(request, username):
    """Профайл пользователя"""
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "user": user,
        "page": page
    }
    return render(request, "profile.html", context)


def post_view(request, username, post_id):
    """Просмотр записи"""
    post = get_object_or_404(Post, id=post_id)
    context = {
        "post": post
    }
    return render(request, "post.html", context)


def post_edit(request, username, post_id):
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    post = get_object_or_404(Post, id=post_id)
    if request.method != "POST":
        form = PostForm(instance=post)
        context = {
            "form": form,
            "is_edit": True,
        }
        return render(request, "post_new.html", context)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        change_post = form.save(commit=False)
        change_post.author = request.user
        change_post.save()
        return redirect("post", username=username, post_id=post_id)
