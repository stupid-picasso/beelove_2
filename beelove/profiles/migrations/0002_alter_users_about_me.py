# Generated by Django 3.2.2 on 2021-05-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='about_me',
            field=models.TextField(default='About Me...'),
        ),
    ]
