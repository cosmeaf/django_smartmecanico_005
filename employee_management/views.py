from rest_framework import viewsets, permissions
from .models import EmployeeInfo
from .serializers import EmployeeInfoSerializer

class IsEmployeeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class EmployeeInfoModelViewSet(viewsets.ModelViewSet):
    queryset = EmployeeInfo.objects.all()
    serializer_class = EmployeeInfoSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associe o usuário atual ao objeto EmployeeInfo antes de salvar.
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsEmployeeOwner]

        return [permission() for permission in permission_classes]