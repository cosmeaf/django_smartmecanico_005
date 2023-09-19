from rest_framework import viewsets, permissions
from .models import Address
from .serializers import AddressSerializer, AddressDetailSerializer

class IsAddressOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permite apenas que o proprietário do endereço acesse a visualização detalhada ou faça alterações
        return obj.user == request.user

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        # Permite que superusuários vejam todos os endereços, enquanto os usuários normais podem ver apenas seus próprios endereços
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Define o usuário atual como proprietário do novo endereço criado
        serializer.save(user=self.request.user)

    def get_permissions(self):
        # Retorna permissões diferentes dependendo da ação executada
        if self.action in ['list', 'create']:
            # Permite que usuários autenticados criem novos endereços e visualizem apenas seus próprios endereços
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Permite que apenas proprietários de endereços atualizem/excluam endereços
            permission_classes = [permissions.IsAuthenticated, IsAddressOwner]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        # Define a classe do serializador com base na ação
        if self.action in ['create', 'list']:
            return AddressSerializer
        return AddressDetailSerializer
