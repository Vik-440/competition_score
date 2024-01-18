"""Serializers for Squad"""

from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)
# from rest_framework import serializers

from squad.models import Squad


class SquadSerializer(ModelSerializer):
    squad_id = IntegerField(source='id', read_only=True)
    nomination_name = SerializerMethodField()
    performance_date_time = DateTimeField(format="%Y-%m-%d %H:%M")

    def get_nomination_name(self, obj: Squad) -> str:
        return obj.nomination_id.nomination_name

    class Meta:
        model = Squad
        # fields = '__all__'
        fields = ['squad_id', 'squad_name', 'performance_date_time', 'nomination_id', 'nomination_name']
        read_only_fields = ['squad_id', 'nomination_name']
