""""Database models."""

from django.db.models import (
    CharField,
    EmailField,
    BooleanField,
    ForeignKey,
    CASCADE,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from community.models import Community


class UserManager(BaseUserManager):
    """manager for user."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    
    def create_coach(self, email, password=None, **extra_fields):
        """Create and return new coach."""
        user = self.create_user(email, password, **extra_fields)
        user.is_coach = True
        user.save(using=self._db)

        return user
    
    def create_judge(self, email, password=None, **extra_fields):
        """Create and return new judge."""
        user = self.create_user(email, password, **extra_fields)
        user.is_judge = True
        user.save(using=self._db)

        return user
    
    def create_observer(self, email, password=None, **extra_fields):
        """Create and return new observer."""
        user = self.create_user(email, password, **extra_fields)
        user.is_observer = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = EmailField(max_length=255, unique=True)
    name = CharField(max_length=255)
    community_id = ForeignKey(Community, on_delete=CASCADE, null=True, blank=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    is_coach = BooleanField(default=False)
    is_judge = BooleanField(default=False)
    is_observer = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['community']

    def __str__(self):
        return self.name
#         return f'"name" = {self.name}, \
# "email" = {self.email}, "community" = {self.community_id}'