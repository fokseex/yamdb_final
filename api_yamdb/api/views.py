from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (AdminOnly, AdminOrReadOnly,
                          AuthorOrModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReadTitleSerializer,
                          ReviewSerializer, SelfUserSerializer,
                          SignUpSerializer, TitleSerializer, TokenSerializer,
                          UserSerializer)
from .settings import SIGNUP_EMAIL_MESSAGE


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet произведений"""
    queryset = Title.objects.all().annotate(
        Avg("review__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (AdminOrReadOnly,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleSerializer
        return ReadTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet отзывов"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet комментариев"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrReadOnly, )

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями, доступно только администраторам.
    endpoints:
    GET, POST /api/v1/users/ - получить список пользователей,
    или создать нового пользователя.
    GET, POST, PATH, DELETE /api/v1/users/{username}/
    - Управление пользователем {username}
    Обязательные поля: username, email
    Необязательные поля: first_name, last_name, bio, role
    """
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    queryset = User.objects.all()


class SignUpViewSet(APIView):
    """
    Регистрация нового пользователя, принимает только POST запросы.
    Использование /api/v1/auth/signup/
    data:
    {
    "email": "string",
    "username": "string"
     }.
    После успешной регистрации будет на указанный email будет отправлено
    письмо с кодом для получения и обновления токена.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = user.confirmation_code
            email = user.email
            send_mail(
                SIGNUP_EMAIL_MESSAGE['theme'],
                SIGNUP_EMAIL_MESSAGE['message'] + confirmation_code,
                SIGNUP_EMAIL_MESSAGE['sender'],
                [email, ]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class GetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Получение нового токена и обновление существующего.
    endpoint: /api/v1/auth/token/
    data:
    {
    "email": "string",
    "confirmation_code": "string"
     }
    response: {"token": "string"}
    """
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)


class SelfUserViewSet(APIView):
    """
    Управление собственными данными пользователя.
    endpoint: /api/v1/users/me/ - GET, PATH
    data:
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user" - read only
    }
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user
        serializer = SelfUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = SelfUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
