from django.urls import path
from blog.views.blog_views import BlogView,SingleBlogView


urlpatterns = [
    path("",BlogView,name='blog'),
    path('single/',SingleBlogView,name='single'),

    
]
