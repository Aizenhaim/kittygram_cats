from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from cats.models import Cat
from .models import Destination, Travel
from .permissions import IsCatOwnerOrReadOnly
from .serializers import DestinationSerializer, TravelSerializer


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name', 'country']
    ordering = ['country', 'name']
    pagination_class = PageNumberPagination


class TravelViewSet(viewsets.ModelViewSet):
    queryset = Travel.objects.select_related('cat', 'destination').all()
    serializer_class = TravelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCatOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['cat', 'destination', 'status']
    ordering_fields = ['departure_date', 'status']
    ordering = ['-departure_date']
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        cat = serializer.validated_data['cat']
        if cat.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Вы можете планировать путешествия только для своих котов.')
        serializer.save()

    @action(detail=False, methods=['get'], url_path='my')
    def my_travels(self, request):
        """Путешествия котов текущего пользователя."""
        cat_ids = Cat.objects.filter(owner=request.user).values_list('id', flat=True)
        travels = Travel.objects.filter(cat__in=cat_ids).select_related('cat', 'destination')
        page = self.paginate_queryset(travels)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(travels, many=True)
        return Response(serializer.data)
