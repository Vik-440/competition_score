# Generated by Django 4.2.4 on 2023-09-07 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports_person', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='ranksportsperson',
            name='rank',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='team',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
