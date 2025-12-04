"""
Система разрешений для REST API приложения books.

Реализует ролевой контроль доступа:
- Администратор: полный доступ (CRUD)
- Менеджер: создание и редактирование (без удаления)
- Пользователь: только чтение
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение для администраторов: полный доступ.
    Остальные пользователи могут только читать.
    """
    
    def has_permission(self, request, view):
        # Разрешаем чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Для изменения требуется аутентификация и роль администратора
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role == 'admin'
        )


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Разрешение для менеджеров и администраторов: создание и редактирование.
    Удаление доступно только администраторам.
    Остальные пользователи могут только читать.
    """
    
    def has_permission(self, request, view):
        # Разрешаем чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Для удаления требуется роль администратора
        if request.method == 'DELETE':
            return (
                request.user and
                request.user.is_authenticated and
                hasattr(request.user, 'role') and
                request.user.role == 'admin'
            )
        
        # Для создания и редактирования требуется роль менеджера или администратора
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role in ['admin', 'manager']
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение для владельца объекта: полный доступ к своему объекту.
    Остальные пользователи могут только читать.
    """
    
    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Проверяем, является ли пользователь владельцем объекта
        # Для Review проверяем связь через book (если есть user в Review)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Для других объектов проверяем created_by или owner
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        # Если нет явного владельца, разрешаем только администраторам
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role == 'admin'
        )

