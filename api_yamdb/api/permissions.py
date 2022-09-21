from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrReadOnly(BasePermission):
    """Доступ на чтение для всех с правами ниже администратора"""

    def has_permission(self, request, view) -> bool:
        """Только администратор имеет доступ на запись"""
        if request.user.is_authenticated:
            return any(
                (request.method in SAFE_METHODS, request.user.is_admin())
            )
        return request.method in SAFE_METHODS


class AuthorOrModeratorOrReadOnly(BasePermission):
    """
    Неавторизованный пользователь имеет доступ на чтение.
    Все авторизованные пользователи могут создавать объект.
    Только автор объекта и модератор имеют права на доступ к объекту.
    """

    def has_permission(self, request, view):
        """Доступ неавторизованных пользователей только на чтение"""
        return any(
            (request.method in SAFE_METHODS, request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        """
        Любой авторизованный пользователь может создать объект,
        Доступ на чтение только у автора и модератора.
        """
        if request.user.is_authenticated:
            return any(
                (
                    request.user.is_moderator(),
                    request.user == obj.author,
                    view.action == 'retrieve'
                )
            )
        return view.action == 'retrieve'


class AdminOnly(BasePermission):
    """Доступ только у пользователя с правами администратора"""

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and request.user.is_admin()
