from django.contrib import admin
from comment.models.comment_models import Comment




class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('post_id','id','author','approved','created_date')
    list_filter = ('created_date','approved')
    search_fields = ['created_date']



admin.site.register(Comment,CommentAdmin)