# Generated by Django 4.2.4 on 2023-09-29 17:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports_person', '0005_sportsperson_gender_sportsperson_height_cm_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonRank',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('person_rank_name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('person_rank_weight', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.RemoveField(
            model_name='sportsperson',
            name='rank',
        ),
        migrations.AlterField(
            model_name='sportsperson',
            name='height_cm',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(250)]),
        ),
        migrations.AlterField(
            model_name='sportsperson',
            name='weight_kg',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(200)]),
        ),
        migrations.AddField(
            model_name='sportsperson',
            name='person_rank_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sports_person.personrank'),
        ),
    ]