from rest_framework import routers, serializers, viewsets

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'registration', 'brand', 'type', 'owner']


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return Vehicle.objects.all()
        return user.vehicle_set.all()


router = routers.DefaultRouter()
router.register(r'vehicle', VehicleViewSet)
