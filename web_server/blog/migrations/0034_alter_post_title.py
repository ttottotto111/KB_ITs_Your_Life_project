# Generated by Django 3.2 on 2022-05-17 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_auto_20220517_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, choices=[('캐스퍼', '캐스퍼'), ('소나타', '소나타')], max_length=30, null=True),
        ),
    ]