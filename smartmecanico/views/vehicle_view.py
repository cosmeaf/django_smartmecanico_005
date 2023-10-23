from rest_framework import viewsets, permissions
from security.models import CustomUser
from smartmecanico.models.vehicle_model import Vehicle
from smartmecanico.serializers.vehicle_serializers import VehicleSerializer, VehicleDetailSerializer

class IsVehicleOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user

class VehicleModelViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_staff and 'user' in serializer.validated_data:
            user_email = serializer.validated_data['user'].email
            user = CustomUser.objects.get(email=user_email)
            serializer.save(user=user)
        else:
            serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsVehicleOwner]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'list']:
            return VehicleSerializer
        return VehicleDetailSerializer
