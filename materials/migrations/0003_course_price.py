# Generated by Django 5.1.4 on 2025-01-06 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(default=100),
        ),
    ]
