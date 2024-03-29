# Generated by Django 4.2.4 on 2023-10-12 17:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomination', '0004_alter_conditionperformance_max_age_person_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditionperformance',
            name='max_qty_person',
            field=models.IntegerField(default=None, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='conditionperformance',
            name='min_qty_person',
            field=models.IntegerField(default=None, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
