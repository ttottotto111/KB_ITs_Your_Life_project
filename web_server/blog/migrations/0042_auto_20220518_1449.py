# Generated by Django 3.2 on 2022-05-18 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_auto_20220518_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='브랜드',
            field=models.CharField(blank=True, choices=[], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='차종',
            field=models.CharField(blank=True, choices=[], max_length=50, null=True),
        ),
    ]
