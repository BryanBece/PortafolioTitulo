# Generated by Django 5.0.1 on 2024-04-24 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0002_remove_paciente_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
