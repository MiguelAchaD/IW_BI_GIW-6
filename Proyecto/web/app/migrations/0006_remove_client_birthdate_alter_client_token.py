# Generated by Django 4.2.6 on 2023-10-31 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_client_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='birthDate',
        ),
        migrations.AlterField(
            model_name='client',
            name='token',
            field=models.CharField(auto_created='ck1NgURIC6U2wUKg9rlG', max_length=20, unique=True),
        ),
    ]
