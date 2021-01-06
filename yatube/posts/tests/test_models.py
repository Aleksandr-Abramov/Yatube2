from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from ..models import Group, Post

class ModelFieldsTest(TestCase):
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

    def test_post_model_fields(self):
        """Тест значений полей модели Post"""
        field_verboses = {
            "author": "Автор поста",
            "text": "текст",
            "group": "Название сообщества"
        }
        for field, value in field_verboses.items():
            self.assertEqual(self.post._meta.get_field(field).verbose_name, value)