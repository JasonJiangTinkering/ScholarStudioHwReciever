# Generated by Django 3.2.6 on 2022-02-11 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0009_presetchallenger_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presetchallenger',
            name='GameChallenger',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.gamechallenger'),
        ),
    ]
