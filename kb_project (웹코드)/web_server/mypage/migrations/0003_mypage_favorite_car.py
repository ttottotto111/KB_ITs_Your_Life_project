# Generated by Django 4.0.4 on 2022-05-18 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0002_alter_mypage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypage',
            name='favorite_car',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
