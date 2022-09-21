from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .validators import UsernameValidator


class CategorySerializer(serializers.ModelSerializer):
    """Serializer категорий"""
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Serializer жанров"""
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Serializer произведений"""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')


class ReadTitleSerializer(serializers.ModelSerializer):
    """Serializer произведений только для чтения"""
    rating = serializers.IntegerField(source='review__score__avg',
                                      read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    """Create new user."""
    class Meta:
        model = User
        fields = ('username', 'email')
        read_only_fields = ('confirmation_code',)
        validators = (UsernameValidator(fields=('username',)),)


class TokenSerializer(serializers.Serializer):
    """Check user confirmation code and return access token."""
    username = serializers.CharField(required=True, write_only=True)
    confirmation_code = serializers.CharField(
        required=True,
        max_length=12,
        write_only=True
    )
    token = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        return User(**validated_data)

    def get_token(self, obj):
        """Create token for user."""
        user = get_object_or_404(User, username=obj.username)
        token = RefreshToken.for_user(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        return str(token.access_token)

    def validate(self, data):
        """Validate user confirmation code."""
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения!')
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serialize users objects for admin."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        validators = (UsernameValidator(fields=('username',)),)


class SelfUserSerializer(serializers.ModelSerializer):
    """Serialize user objects for self user page."""
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        read_only_fields = ('role',)
        validators = (UsernameValidator(fields=('username',)),)
