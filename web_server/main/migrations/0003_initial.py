# Generated by Django 4.0.4 on 2022-05-12 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_delete_user_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='maker_test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maker', models.CharField(max_length=10)),
            ],
        ),
    ]
