# Generated by Django 4.2.4 on 2023-09-27 10:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports_person', '0004_alter_sportsperson_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportsperson',
            name='gender',
            field=models.CharField(choices=[('men', 'men'), ('women', 'woman')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='sportsperson',
            name='height_cm',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='sportsperson',
            name='weight_kg',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='sportsperson',
            name='city',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='sportsperson',
            name='rank',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='sportsperson',
            name='team',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
