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
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
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
    community_id = IntegerField()

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        community_id = attrs.get('community_id')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise ValidationError(msg, code='authorization')
        if user.community_id != community_id:
            raise ValidationError(_("User does not belong to this community."), code='authorization')

        attrs['user'] = user
        return attrs
