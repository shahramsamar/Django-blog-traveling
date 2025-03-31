from django.contrib import admin
from blog.models.blog_models import Post, Category, NewsLetter


class PostAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "title",
        "views",
        "is_published",
        "created_date",
        "updated_date",
    ]
    search_fields = ["title", "content"]
    list_filter = ("author", "is_published")
    empty_value_display = "-empty-"
    date_hierarchy = "created_date"


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(NewsLetter)
