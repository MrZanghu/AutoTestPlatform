# Generated by Django 3.2 on 2023-04-27 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_platform', '0010_alter_jobexecuted_status'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='jobexecuted',
            table='atp_job_executed',
        ),
    ]
