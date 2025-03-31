# Generated by Django 5.1.7 on 2025-03-23 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("blog", "0004_newsletter_alter_post_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(default="user.jpeg", upload_to="")),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=100)),
                ("subject", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("approved", models.BooleanField(default=False)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateField(auto_now=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.post"
                    ),
                ),
            ],
            options={
                "ordering": ["created_date"],
            },
        ),
    ]
