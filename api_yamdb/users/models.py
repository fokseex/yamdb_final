from typing import List, Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from api_yamdb.settings import PRIVILEGE_LEVELS


class User(AbstractUser):
    """
    Расширение стандартного пользователя Django. Для
    проверки ролей пользователя используется функция is_<role>.
    """
    ROLE_CHOICES: List[Tuple[int, str]] = [
        (key, key) for key in PRIVILEGE_LEVELS
    ]
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        help_text='Напишите информацию о себе'
    )
    role = models.CharField(
        max_length=10,
        verbose_name='Роль пользователя',
        help_text='Выберете роль пользователя',
        default='user',
        choices=ROLE_CHOICES
    )
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
    )
    confirmation_code = models.CharField(
        max_length=12,
        default=get_random_string,
        editable=False,
    )
    password = models.CharField(_('password'), max_length=128, blank=True)

    class Meta:
        ordering = ['id']

    def is_moderator(self) -> bool:
        """Есть ли права модератора или выше"""
        return PRIVILEGE_LEVELS[self.role] >= 2 or self.is_superuser

    def is_admin(self) -> bool:
        """Есть ли права администратора или выше"""
        return PRIVILEGE_LEVELS[self.role] == 3 or self.is_superuser
