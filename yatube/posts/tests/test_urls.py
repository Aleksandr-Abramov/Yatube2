from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ..models import Group, Post


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Тестовые данные"""
        cls.user = get_user_model().objects.create_user(username="Leon")

        cls.list_pages = {
            reverse("index"): "index.html",
            reverse("group_post", args=["test-lev"]): "group.html",
        }

        cls.group = Group.objects.create(
            title="Заголовок группы",
            slug="test-lev",
            description="Тестовый текст группы"
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый текст поста"
        )

    def setUp(self) -> None:
        """Тестовые пользователи"""
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(username="Alex")
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_all_pages_urls(self):
        """Проверка страниц на статус 200"""
        for page, templates in self.list_pages.items():
            response = self.guest_client.get(page)
            self.assertEqual(response.status_code, 200,
                             f"Страница {page} не работает")

    def test_all_templates(self):
        """Проверка шаблонов"""
        for page, templates in self.list_pages.items():
            response = self.guest_client.get(page)
            self.assertTemplateUsed(response, templates,
                                    f"Шаблон {templates} не работае")

    # def test_index_url(self):
    #     """Тест index.html код 200"""
    #     response = self.guest_client.get(reverse("index"))
    #     self.assertEqual(response.status_code, 200, "Не возврощает код 200")

    # def test_index_page_template(self):
    #     """Тест index.html шаблон"""
    #     response = self.guest_client.get(
    #         reverse("group_post", kwargs={"slug": "test-lev"}))
    #     self.assertEqual(response.status_code, 200, "Не возврощает код 200")
    #     self.assertTemplateUsed(response, "group.html", "Шаблон не работает")
