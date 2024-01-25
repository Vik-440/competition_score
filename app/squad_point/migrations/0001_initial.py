# Generated by Django 4.2.4 on 2024-01-25 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('judge_person', '0003_judgeperson_gender_judgeperson_height_cm_and_more'),
        ('squad', '0003_alter_squad_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SquadPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judge_person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge_person.judgeperson')),
                ('squad_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='squad.squad')),
            ],
            options={
                'unique_together': {('squad_id', 'judge_person_id')},
            },
        ),
    ]