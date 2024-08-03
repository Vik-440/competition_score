"""Serializers for crossing users and communities."""

from django_filters import (
    FilterSet,
    NumberFilter)
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
)
from user_community.models import UserCommunity
from community.models import Community
from core.models import User


class UserCommunityFilter(FilterSet):
    """Filter for user and community in UserCommunity"""
    user_id = NumberFilter(field_name='user_id', lookup_expr='exact')
    community_id = NumberFilter(
        field_name='community', lookup_expr='exact')

    class Meta:
        model = UserCommunity
        fields = ['user_id', 'community_id']


class UserCommunitySerializer(ModelSerializer):
    """Serializers for UserCommunity"""
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all())
    community_id = PrimaryKeyRelatedField(
        queryset=Community.objects.all())
    
    class Meta:
        model = UserCommunity
        fields = '__all__'
        read_only_fields = ('id', )
    
