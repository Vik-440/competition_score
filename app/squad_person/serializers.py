"""Serializers for Squad cross SportsPerson"""

from rest_framework.serializers import (
    ModelSerializer,
)

from squad_person.models import SquadPerson


class SquadPersonSerializer(ModelSerializer):

    class Meta:
        model = SquadPerson
        fields = '__all__'
        read_only_fields = ['id']
