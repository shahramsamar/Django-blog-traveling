from django.urls import path
from blog.views.blog_views import BlogView


urlpatterns = [
    path("",BlogView,name='blog'),

    
]
