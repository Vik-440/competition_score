from django.db import models
from django.core.validators import MinLengthValidator


class JudgePerson(models.Model):
    """JudgePerson object."""
    GENDER_CHOICES = (
        ('men', 'men'),
        ('women', 'woman'),
    )

    first_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)])
    last_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)])
    birth_day = models.DateField()
    team = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)], null=True)
    rank = models.CharField(
        max_length=50, validators=[MinLengthValidator(3)], null=True)
    license_expiration_date = models.DateField()
    gender = models.CharField(
        max_length=15,
        choices=GENDER_CHOICES,
        null=True,
    )
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}, {self.rank}'

    class Meta:
        unique_together = ('first_name', 'last_name', 'rank')
