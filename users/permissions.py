from rest_framework import permissions


class OwnProfileOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user.profile
    

class IsAuthenticatedAndIsCraftsman(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return bool (request.user and request.user.is_authenticated
                and request.user.profile.is_craftsman)


class IsCutomerOrProvider(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user.profile or obj.provider == request.user.profile
