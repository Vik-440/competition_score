"""serializers for community of groups"""

from rest_framework.serializers import (
    ModelSerializer,
)

from django_filters import (
    FilterSet,
    CharFilter,
    BooleanFilter,
)

from community.models import Community


class CommunityFilter(FilterSet):
    """Filter for return communities from DB"""
    name = CharFilter(field_name='name', lookup_expr='contains')
    status = BooleanFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Community
        fields = ['name', 'status']


class CommunitySerializer(ModelSerializer):
    """Serializer for Community"""

    class Meta:
        model = Community
        fields = '__all__'
        read_only_fields = ['id']
