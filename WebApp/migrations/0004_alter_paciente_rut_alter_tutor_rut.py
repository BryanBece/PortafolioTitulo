# Generated by Django 5.0.3 on 2024-04-27 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0003_alter_tutor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='rut',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='rut',
            field=models.CharField(max_length=12),
        ),
    ]
