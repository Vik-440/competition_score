# Generated by Django 4.2.4 on 2023-09-27 10:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge_person', '0002_alter_judgeperson_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='judgeperson',
            name='gender',
            field=models.CharField(choices=[('men', 'men'), ('women', 'woman')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='judgeperson',
            name='height_cm',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='judgeperson',
            name='weight_kg',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='judgeperson',
            name='rank',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='judgeperson',
            name='team',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]