# Generated by Django 5.1.7 on 2025-03-30 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0010_rename_message_comment_content"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="approved",
        ),
    ]
