from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Читать могут все. Изменять (POST, PUT, DELETE) — только админ.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Редактировать объект может только его владелец.
    Добавлена защита: если у объекта нет поля 'user', но есть 'build',
    проверяем владельца сборки.
    """
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, 'user'):
            return obj.user == request.user

        if hasattr(obj, 'build'):
            return obj.build.user == request.user
        return False