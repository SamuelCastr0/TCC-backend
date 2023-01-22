# Generated by Django 4.1.4 on 2023-01-08 21:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0004_course_courselearningobject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['createdAt']},
        ),
        migrations.AlterModelOptions(
            name='courselearningobject',
            options={'ordering': ['index']},
        ),
        migrations.AddField(
            model_name='course',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]