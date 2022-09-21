from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenViewSet, ReviewViewSet, SelfUserViewSet,
                    SignUpViewSet, TitleViewSet, UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register('auth/token', GetTokenViewSet, basename='token')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/users/me/', SelfUserViewSet.as_view(), name='me'),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
]
