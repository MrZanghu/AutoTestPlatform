# Generated by Django 3.2 on 2023-05-22 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_platform', '0017_auto_20230520_1714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='realm_name',
            new_name='is_https',
        ),
    ]