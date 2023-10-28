# Generated by Django 4.2.6 on 2023-10-28 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_module_selectedmodules_purchase_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='client',
            name='username',
        ),
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='id',
            field=models.CharField(default='QQKB4IRiZeDGLDkgZWm2', max_length=20, primary_key=True, serialize=False),
        ),
    ]
