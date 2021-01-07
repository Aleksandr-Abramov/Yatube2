from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ..forms import PostForm
from ..models import Group, Post


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Тестовые данные"""
        cls.form = PostForm()
        cls.user = get_user_model().objects.create_user(username="Alex")
        cls.group = Group.objects.create(
            title="Заголовок группы",
            slug="test-lev",
            description="Тестовый текст группы"
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="тестовый текст поста",
            group=cls.group
        )

    def setUp(self) -> None:
        """Тестовые пользователи"""
        self.user = get_user_model().objects.create_user(username="Leon")
        self.authorized_guest = Client()
        self.authorized_guest.force_login(self.user)

    def test_create_post_and_redirect(self):
        """Тест код 200, редирект и сохранения данных"""
        form_data = {
            "text": "test-text",
            "group": self.group.id
        }

        tasks_count = Post.objects.count()
        response = self.authorized_guest.post(
            reverse("new_post"),
            data=form_data,
            follow=True)
        self.assertEqual(response.status_code, 200, "Страница new.html не отвечает")
        self.assertRedirects(response, "/")
        self.assertEqual(Post.objects.count(), tasks_count + 1,
                         f"Количество постов меньше {tasks_count + 1}")

    def test_change_post_and_redirect(self):
        """Тест код 200, редирект и изменение данных"""
        form_data = {
            "text": "test-text",
            "group": self.group.id
        }

        response = self.authorized_guest.post(
            reverse("post_edit", args=[self.user, 1]),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200,
                         "Страница post_new.html не отвечает")
        self.assertEqual(Post.objects.first().text, form_data["text"],
                         "Пост не миняется.")
        self.assertRedirects(
            response,
            reverse("post", args=[self.user, self.post.id]))
