from rest_framework.exceptions import ValidationError


class UsernameValidator:
    """Checks that the value in the username field is not equal to 'me'."""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, attrs):
        checked_values = [
            value for field, value in attrs.items() if field in self.fields
        ]
        if 'me' in checked_values:
            raise ValidationError(
                'Для поля username нельзя использовать имя me'
            )
