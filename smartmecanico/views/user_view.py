from rest_framework import viewsets, permissions
from security.models import CustomUser
from smartmecanico.serializers.user_serializers import CustomUserSerializer

class IsUserOwner(permissions.BasePermission):
    """
    Permissão personalizada que permite superusuários fazerem qualquer coisa,
    enquanto usuários normais só podem manipular seus próprios registros.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj == request.user

class CustomUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        if self.request.user.is_superuser and 'user' in self.request.data:
            user_email = self.request.data.get('user')
            user = CustomUser.objects.get(email=user_email)
            serializer.save(user=user)
        else:
            serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsUserOwner]

        return [permission() for permission in permission_classes]
