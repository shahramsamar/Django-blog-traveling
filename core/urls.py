"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="blog api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="shahramsamar2010@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)







from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls.blog-urls")),
    path('accounts/', include('accounts.urls.accounts_urls')),
  

    # api documents
    path("api-auth/", include("rest_framework.urls")),
    path("accounts/drf/", include('accounts.api.v1.furls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
