from django.db.models import (
    Model,
    CharField,
    DateField,
    DecimalField,
    IntegerField,
    ForeignKey,
    AutoField,
    SET_NULL,
)
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)


class SportsPerson(Model):
    """SportsPerson object."""
    GENDER_CHOICES = (
        ('men', 'men'),
        ('women', 'woman'),
    )

    first_name = CharField(max_length=50, validators=[MinLengthValidator(3)])
    last_name = CharField(max_length=50, validators=[MinLengthValidator(3)])
    birth_day = DateField()
    city = CharField(
        max_length=50, validators=[MinLengthValidator(3)], null=True)
    team = CharField(
        max_length=50, validators=[MinLengthValidator(3)], null=True)
    # rank = CharField(
    #     max_length=50, validators=[MinLengthValidator(3)], null=True)
    person_rank_id = ForeignKey('PersonRank', on_delete=SET_NULL, null=True)
    gender = CharField(
        max_length=15,
        choices=GENDER_CHOICES,
        null=True,)
    weight_kg = DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        validators=[MinValueValidator(10), MaxValueValidator(200)])
    height_cm = DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        validators=[MinValueValidator(50), MaxValueValidator(250)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}, \
            {self.person_rank_id}, {self.team}'

    class Meta:
        unique_together = ('first_name', 'last_name', 'birth_day')


class PersonRank(Model):
    """SportPerson ranks"""
    id = AutoField(primary_key=True)
    person_rank_name = CharField(
        max_length=50,
        validators=[MinLengthValidator(3)],
        null=False,
        unique=True)
    person_rank_weight = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False,)

    def __str__(self):
        return f'{self.person_rank_name}: {self.person_rank_weight}'
