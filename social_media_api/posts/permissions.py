from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    إذن مخصص يسمح فقط لمؤلف الكائن بتعديله أو حذفه.
    """
    def has_object_permission(self, request, view, obj):
        # السماح بالقراءة (GET, HEAD, OPTIONS) لأي طلب
        if request.method in permissions.SAFE_METHODS:
            return True

        # السماح بالكتابة (PUT, PATCH, DELETE) فقط لمؤلف الكائن
        return obj.author == request.user