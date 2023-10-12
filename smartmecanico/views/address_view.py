from rest_framework import status, serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from security.models import CustomUser
from smartmecanico.models.address_model import Address
from smartmecanico.serializers.address_serializers import AddressSerializer 


# VIEW ADDRESS
class IsAddressOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class AddressModelViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
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

