from django.db import models
from django.core.validators import MinLengthValidator


class JudgePerson(models.Model):
    """JudgePerson object."""

    first_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)])
    last_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)])
    birth_day = models.DateField()
    # city = models.CharField(
    #     max_length=50, validators=[MinLengthValidator(3)], default=None)
    team = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)], default=None)
    rank = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)], default=None)
    license_expiration_date = models.DateField()

    def __str__(self):
        return f'{self.last_name} {self.first_name}, {self.rank}'

    class Meta:
        unique_together = ('first_name', 'last_name', 'birth_day')
