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
    path("archive/<int:year>/<int:month>/",blog_views.MonthlyArchiveView.as_view(month_format='%m'),name='post_archive'),

    path("post/<int:pk>/", blog_views.SingleBlogView.as_view(), name='single'),
]
