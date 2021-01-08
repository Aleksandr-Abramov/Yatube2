from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django import forms
from django.core.paginator import Paginator

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
        expected_content = response.context.get("page")[0]
        self.assertEqual(content, expected_content,
                         "Контекст index.html не верен")

    def test_group_post_content(self):
        """Проверка контента group.html"""
        response = self.guest_client.get(reverse("group_post", args=["test-lev"]))
        content = self.post
        expected_content = response.context.get("posts")[0]
        self.assertEqual(content, expected_content,
                         "Контекст group.html не верен")

    def test_post_view_content(self):
        """Проверка контента post.html"""
        response = self.authorized_user.get(
            reverse("post", kwargs={"username": self.user, "post_id": 1}))
        content = self.post
        expected_content = response.context.get("post")
        self.assertEqual(content, expected_content)

    def test_new_post_form(self):
        """Проверка полей формы для new_post add_or_change_post.html"""
        fields_list = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        response = self.authorized_user.get(reverse("new_post"))
        for field, field_widget in fields_list.items():
            form_field = response.context.get('form').fields.get(field)
            self.assertIsInstance(form_field, field_widget)

    def test_post_edit_form(self):
        """Проверка полей формы для post_edit add_or_change_post.html"""
        fields_list = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        response = self.authorized_user.get(
            reverse("post_edit", args=[self.user, self.post.id]))

        for field, field_widget in fields_list.items():
            form_field = response.context.get('form').fields.get(field)
            self.assertIsInstance(form_field, field_widget)

    def test_create_content_index(self):
        """Тест создания поста index.html"""
        new_post = Post.objects.create(
            text="тестовый текст",
            author=self.user,
            group=self.group
        )
        response = self.authorized_user.get(
            reverse("index"))
        self.assertContains(response, new_post)

    def test_create_content_group(self):
        """Тест создания поста group.html"""
        new_post = Post.objects.create(
            text="тестовый текст",
            author=self.user,
            group=self.group
        )
        response = self.authorized_user.get(
            reverse("group_post", args=[self.group.slug]))
        self.assertContains(response, new_post)


class PaginatorViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Тестовые данные"""
        cls.user = get_user_model().objects.create_user("Alex")

        cls.group = Group.objects.create(
            title="Заголовок группы",
            slug="test-lev",
            description="Тестовый текст группы"
        )

        for i in range(13):
            Post.objects.create(
                text=f"тестовый текст{i}",
                author=cls.user,
                group=cls.group
            )

    def setUp(self) -> None:
        self.guest_client = Client()

    def test_paginator_first_page(self):
        """Тест количества постов на странице"""
        response = self.guest_client.get(reverse("index"))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_paginator_second_page(self):
        """Тест количества постов на второй странице"""
        response = self.guest_client.get(reverse("index") + "?page=2")
        self.assertEqual(len(response.context.get('page').object_list), 3)
