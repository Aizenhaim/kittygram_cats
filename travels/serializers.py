import datetime as dt

from rest_framework import serializers

from cats.models import Cat
from cats.serializers import CatSerializer
from .models import Destination, Travel


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('id', 'name', 'country', 'description')


class TravelSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(), source='destination', write_only=True
    )
    cat_detail = CatSerializer(source='cat', read_only=True)
    cat = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.all())

    class Meta:
        model = Travel
        fields = (
            'id', 'cat', 'cat_detail', 'destination', 'destination_id',
            'departure_date', 'arrival_date', 'status', 'notes',
        )

    def validate(self, data):
        arrival = data.get('arrival_date')
        departure = data.get('departure_date')
        if arrival and departure and arrival < departure:
            raise serializers.ValidationError(
                'Дата прибытия не может быть раньше даты отправления!'
            )
        status = data.get('status', Travel.STATUS_PLANNED)
        if status == Travel.STATUS_PLANNED and departure:
            if departure < dt.date.today():
                raise serializers.ValidationError(
                    'Дата отправления не может быть в прошлом для запланированного путешествия!'
                )
        return data
