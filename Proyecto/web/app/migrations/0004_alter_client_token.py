# Generated by Django 4.2.6 on 2023-11-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_client_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='token',
            field=models.CharField(auto_created='vPTq8e6BgR8Ekn7yhb8i', max_length=20, unique=True),
        ),
    ]
