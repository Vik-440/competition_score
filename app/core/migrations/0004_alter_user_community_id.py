# Generated by Django 4.2.4 on 2024-08-04 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_alter_community_background_url'),
        ('core', '0003_user_community_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='community_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.community'),
        ),
    ]