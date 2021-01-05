from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """Модель создания поста"""
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(
        "Group", on_delete=models.CASCADE,
        verbose_name="Название сообщества",
        blank=True, null=True,
        related_name="group"
    )


class Group(models.Model):
    """Модель для Группы"""
    title = models.CharField(verbose_name="Заголовок сообщества", max_length=255)
    slug = models.SlugField(verbose_name="Адрес сообщества в интернете", unique=True)
    description = models.TextField(verbose_name="Описание сообщества")

    def __str__(self):
        return self.title
