# Generated by Django 4.1.2 on 2022-11-19 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='category',
            field=models.CharField(blank=True, choices=[('GRADUATE', 'Graduate Student'), ('MASTERING', 'Mastering Student'), ('PHD', 'PHD Student'), ('PROFESSOR', 'Professor')], default='GRADUATE', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='course',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='github',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='googleScholar',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='lattes',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='oia',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='orcid',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='researchGate',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]