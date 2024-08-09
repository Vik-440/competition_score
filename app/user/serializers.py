"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    EmailField,
    CharField,
    IntegerField,
    PrimaryKeyRelatedField,
    ValidationError,
)
from community.models import Community
from core.models import User


class UserSerializer(ModelSerializer):
    """Serializer for the user object."""
    community_id = PrimaryKeyRelatedField(queryset=Community.objects.all())

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'groups': {'read_only': True},
            'user_permissions': {'read_only': True},
            'last_login': {'read_only': True},
            }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)
        validated_data.pop('last_login', None)
        user = get_user_model().objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)
        validated_data.pop('last_login', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(Serializer):
    """Serializer for the user auth token."""
    email = EmailField()
    password = CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
