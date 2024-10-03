# Generated by Django 5.1 on 2024-08-16 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_driver_alter_order_endtime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.CharField(default='未接单', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='endtime',
            field=models.CharField(default='未完成', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='score',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
