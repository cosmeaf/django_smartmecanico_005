from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from security.models import CustomUser
from smartmecanico.serializers.user_serializers import CustomUserSerializer

# VIEW CUSTOMUSER
class IsCustomUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class CustomUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsCustomUserOwner]

        return [permission() for permission in permission_classes]