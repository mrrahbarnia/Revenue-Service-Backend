# Generated by Django 5.0.6 on 2024-07-16 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]