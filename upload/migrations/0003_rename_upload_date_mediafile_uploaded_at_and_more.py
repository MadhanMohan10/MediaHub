# Generated by Django 4.2.2 on 2024-05-10 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_rename_uploaded_at_mediafile_upload_date_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediafile',
            old_name='upload_date',
            new_name='uploaded_at',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
