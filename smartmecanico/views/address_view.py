from rest_framework import viewsets, permissions
from security.models import CustomUser
from smartmecanico.models.address_model import Address
from smartmecanico.serializers.address_serializers import AddressSerializer, AddressDetailSerializer

class IsAddressOwner(permissions.BasePermission):
    """ 
    Permissão personalizada que permite superusuários verem e alterarem qualquer endereço,
    enquanto usuários normais só podem ver e alterar seus próprios endereços.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user

class AddressModelViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff: 
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Se o usuário logado é superusuário, ele pode especificar qualquer usuário no payload
        if self.request.user.is_staff and 'user' in self.request.data:
            user_email = self.request.data.get('user')
            user = CustomUser.objects.get(email=user_email)
            serializer.save(user=user)
        # Se não, o registro é associado ao usuário logado
        else:
            serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAddressOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'list']:
            return AddressSerializer
        return AddressDetailSerializer
