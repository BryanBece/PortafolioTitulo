# Generated by Django 5.0.3 on 2024-06-01 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0015_oirs_respuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='oirs',
            name='fecha_respuesta',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
