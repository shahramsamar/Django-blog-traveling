from django.urls import path
from blog.views.blog_views import BlogHomeView,SingleBlogView


urlpatterns = [
    path("",BlogHomeView.as_view(),name='blog'),
    path('single/',SingleBlogView,name='single'),

    
]
