from rest_framework import viewsets, filters
from django_filters import rest_framework as django_filters
from smartmecanico.models.services_model import Service, HourService
from smartmecanico.serializers.services_serializers import ServiceSerializer, HourServiceSerializer

class ServiceModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name', 'description'] # Adicione outros campos conforme necessário
    ordering_fields = ['name', 'description'] # Adicione outros campos conforme necessário

class HourServiceModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HourService.objects.all()
    serializer_class = HourServiceSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['hour'] # Adicione outros campos conforme necessário
    ordering_fields = ['hour'] # Adicione outros campos conforme necessário