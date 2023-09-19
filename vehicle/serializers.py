from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'fuel', 'year', 'odometer', 'plate', 'user']

class VehicleDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'fuel', 'year', 'odometer', 'plate', 'user']
        extra_kwargs = {'user': {'required': True}}
