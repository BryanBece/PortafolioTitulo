# Generated by Django 5.0.3 on 2024-06-01 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0012_oirs'),
    ]

    operations = [
        migrations.AddField(
            model_name='oirs',
            name='telefono',
            field=models.CharField(blank=True, max_length=9),
        ),
    ]