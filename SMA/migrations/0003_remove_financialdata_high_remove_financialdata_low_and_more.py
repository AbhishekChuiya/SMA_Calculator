# Generated by Django 4.2.4 on 2023-10-19 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SMA', '0002_rename_timestamp_financialdata_datetime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialdata',
            name='high',
        ),
        migrations.RemoveField(
            model_name='financialdata',
            name='low',
        ),
        migrations.RemoveField(
            model_name='financialdata',
            name='open',
        ),
        migrations.RemoveField(
            model_name='financialdata',
            name='volume',
        ),
    ]