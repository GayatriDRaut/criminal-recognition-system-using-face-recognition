# Generated by Django 3.2.3 on 2022-05-28 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facerecognititon', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='national_id',
            new_name='aadhar_no',
        ),
        migrations.RenameField(
            model_name='thieflocation',
            old_name='national_id',
            new_name='aadhar_no',
        ),
    ]
