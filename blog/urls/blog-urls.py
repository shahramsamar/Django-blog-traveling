from django.urls import path
from blog.views import blog_views


urlpatterns = [
    path("", blog_views.BlogHomeView.as_view(), name='blog'),
    path(
        "category/<str:category>/",
        blog_views.BlogHomeView.as_view(),
        name='blog_category',
    ),
    path("tag/<str:tag>/", blog_views.BlogHomeView.as_view(), name='tag-view'),
    
    path("newsletter/", blog_views.BlogHomeView.as_view(), name='newsletter'),
    
    path("single/", blog_views.SingleBlogView.as_view(), name='single'),
]
