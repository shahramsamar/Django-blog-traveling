from django.contrib import admin
from blog.models.blog_models import Post,Category


class PostAdmin(admin.ModelAdmin):
    
    list_display =[
        'id',
        'title',
        'category',
        'is_published',
        'created_date',
        'updated_date',
    ]

admin.site.register(Post,PostAdmin)
admin.site.register(Category)