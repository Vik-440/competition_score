"""Serializers for Squad"""

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from squad.models import Squad


class SquadSerializer(ModelSerializer):
    nomination_name = SerializerMethodField()

    def get_nomination_name(self, obj: Squad) -> str:
        return obj.nomination_id.nomination_name

    class Meta:
        model = Squad
        fields = '__all__'
        read_only_fields = ['id', 'nomination_name']
