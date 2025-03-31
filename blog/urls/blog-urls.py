from django.urls import path
from blog.views import blog_views


urlpatterns = [
    path("", blog_views.BlogHomeView.as_view(), name="blog"),
    path(
        "category/<str:category>/",
        blog_views.BlogHomeView.as_view(),
        name="category-view",
    ),
    path("tag/<str:tag>/", blog_views.BlogHomeView.as_view(), name="tag-view"),
    path("newsletter/", blog_views.BlogHomeView.as_view(), name="newsletter"),
    path(
        "archive/<int:year>/<int:month>/",
        blog_views.MonthlyArchiveView.as_view(month_format="%m"),
        name="archive-view",
    ),
    path("post/<int:pk>/", blog_views.SingleBlogView.as_view(), name="single"),
    path(
        "post/<int:pk>/comment/",
        blog_views.PostCommentView.as_view(),
        name="add-comment",
    ),
]
