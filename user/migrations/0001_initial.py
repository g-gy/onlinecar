# Generated by Django 5.1 on 2024-08-22 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=15, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=15, verbose_name='密码')),
                ('name', models.CharField(default=None, max_length=5, null=True, verbose_name='姓名')),
                ('detail', models.CharField(default='', max_length=500, verbose_name='个人简介')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photo/', verbose_name='头像')),
                ('car', models.CharField(default='', max_length=15, verbose_name='车牌号')),
                ('money', models.IntegerField(default=0, verbose_name='余额')),
                ('score', models.IntegerField(default=0, verbose_name='评分')),
                ('corder', models.IntegerField(default=0, verbose_name='乘客订单')),
                ('dorder', models.IntegerField(default=0, verbose_name='司机订单')),
            ],
            options={
                'verbose_name': '用户管理',
                'verbose_name_plural': '用户管理',
            },
        ),
    ]
