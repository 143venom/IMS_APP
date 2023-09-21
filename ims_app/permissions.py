from rest_framework import permissions
from rest_framework.permissions import  SAFE_METHODS


class CustomModelPermission(permissions.BasePermission):
    
    # Mapping of HTTP methods to permission codenames.
    METHOD_PERMISSIONS = {
        'GET': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete'
    }

    def has_permission(self, request, view):
        queryset = view.queryset_model.objects.all()

        # Get the type of permission we should be checking based on the HTTP method
        perm_type = self.METHOD_PERMISSIONS.get(request.method, None)
        if not perm_type:
            return False

        app_label = queryset.model._meta.app_label
        model_name = queryset.model._meta.model_name
        full_perm = f"{app_label}.{perm_type}_{model_name}"

        return request.user.has_perm(full_perm)