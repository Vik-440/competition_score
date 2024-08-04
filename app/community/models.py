from django.db.models import (
    Model,
    CharField,
    DateField,
    AutoField,
    BooleanField,
    Index,
    URLField,
)
from django.core.validators import (
    MinLengthValidator,
)


class Community(Model):
    """Models for group which works in one sport area"""
    id = AutoField(primary_key=True)
    name = CharField(
        max_length=50,
        validators=[MinLengthValidator(3)],
        null=False,
        unique=True)
    description = CharField(
        max_length=250,
        null=True)
    expiration_date = DateField()
    status = BooleanField()
    background_url = URLField(max_length=255, null=True, default=None, blank=True)

    def clean(self):
        if self.background_url == '':
            self.background_url = None

    def __str__(self):
        return self.name
#         return f'"id" = {self.id}, "name" = {self.name}, \
# "expiration_date" = {self.expiration_date}, \
# "status" = {self.status}, "description" = ({self.description} \
# "background_url" = {self.background_url})'
    
    class Meta:
        indexes = [
            Index(fields=['status']),
        ]
