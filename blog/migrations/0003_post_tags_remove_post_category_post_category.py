# Generated by Django 5.1.7 on 2025-03-22 08:20

import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_post_content"),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.RemoveField(
            model_name="post",
            name="category",
        ),
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.ManyToManyField(blank=True, to="blog.category"),
        ),
    ]
