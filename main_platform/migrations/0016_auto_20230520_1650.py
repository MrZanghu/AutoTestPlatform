# Generated by Django 3.2 on 2023-05-20 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_platform', '0015_server_realm_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='port',
            field=models.CharField(default='', max_length=50, null=True, verbose_name='端口号'),
        ),
        migrations.AlterField(
            model_name='server',
            name='realm_name',
            field=models.IntegerField(default=0, help_text='0：否，1：是', verbose_name='请求方式为Https'),
        ),
    ]