# Generated by Django 5.1.2 on 2024-10-29 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
