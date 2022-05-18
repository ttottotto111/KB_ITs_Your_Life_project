# Generated by Django 3.2 on 2022-05-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_remove_post_카'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='카',
            field=models.CharField(blank=True, choices=[('S', 'Small'), ('M', 'Medium')], max_length=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]