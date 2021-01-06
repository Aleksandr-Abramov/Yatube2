from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ..models import Post, Group


class ViewContentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Тестовые данные"""
        cls.user = get_user_model().objects.create_user(username="Leon")

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
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(username="Alex")
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_index_content(self):
        """Проверка контента index.html"""
        response = self.guest_client.get(reverse("index"))
        content = self.post
        expected_content = response.context.get("posts")[0]
        self.assertEqual(content, expected_content,
                         "Контекст index.html не верен")

    def test_group_post_content(self):
        """Проверка контента group.html"""
        response = self.guest_client.get(reverse("group_post", args=["test-lev"]))
        content = self.post
        expected_content = response.context.get("posts")[0]
        self.assertEqual(content, expected_content,
                         "Контекст group.html не верен")

