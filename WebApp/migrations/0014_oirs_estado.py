# Generated by Django 5.0.3 on 2024-06-01 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0013_oirs_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='oirs',
            name='estado',
            field=models.CharField(default='Pendiente', max_length=10),
        ),
    ]
