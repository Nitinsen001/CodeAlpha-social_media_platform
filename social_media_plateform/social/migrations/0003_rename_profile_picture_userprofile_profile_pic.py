# Generated by Django 5.2.1 on 2025-06-27 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_rename_text_comment_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_picture',
            new_name='profile_pic',
        ),
    ]
