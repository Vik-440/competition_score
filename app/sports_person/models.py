from django.db import models
from django.core.validators import MinLengthValidator


class SportsPerson(models.Model):
    """SportsPerson object."""

    first_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)])
    last_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)])
    birth_day = models.DateField()
    city = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)], default=None)
    team = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)], default=None)
    rank = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)], default=True)

    def __str__(self):
        return self.last_name

    class Meta:
        unique_together = ('first_name', 'last_name', 'birth_day')
