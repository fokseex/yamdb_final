from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидация года создания произведения"""
    if value > timezone.now().year:
        raise ValidationError('Год не может быть больше текущего')
    elif value < 0:
        raise ValidationError('Год не может быть отрицательным')
