# Generated by Django 4.1.2 on 2024-04-11 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
