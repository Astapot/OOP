from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.permissions import IsOwner
from advertisements.filters import AdvertisementFilter
from rest_framework.authentication import TokenAuthentication

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    serializer_class = AdvertisementSerializer

    # filterset_fields = ['creator', 'status']
    authentication_classes = (TokenAuthentication,)
    # filter_backends = [AdvertisementFilter]
    # filterset_fields = ['created_at']
    # permission_classes = [IsAuthenticated, IsOwner]
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return []

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

