# Generated by Django 4.2.6 on 2023-12-10 16:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_productquantity_cartproduct_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartrelation',
            name='cartProduct',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.cartproduct'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.client'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
