from django.contrib import admin
from comment.models.comment_models import Comment




class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('id','post_id','parent_id','author','content','parent','approved','created_date')
    list_filter = ('created_date','approved','id')
    search_fields = ['created_date','post_id','parent_id']



admin.site.register(Comment,CommentAdmin)