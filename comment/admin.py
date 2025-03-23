from django.contrib import admin
from comment.models.comment_models import Comment




class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('name','post','approved','created_date')
    list_filter = ('post','approved')
    search_fields = ['name','post']



admin.site.register(Comment,CommentAdmin)