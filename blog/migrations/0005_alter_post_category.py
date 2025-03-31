# Generated by Django 5.1.7 on 2025-03-23 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_newsletter_alter_post_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="category",
            field=models.ManyToManyField(
                blank=True, related_name="posts", to="blog.category"
            ),
        ),
    ]
