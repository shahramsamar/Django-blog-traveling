from django.urls import path,include
from accounts.api.v1.fviews import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("token/login/",views.CustomObtainToken,basename ='token-login')
urlpatterns = [
    # login token 
    # path('token/login/',views.CustomObtainToken.as_view(),name='token-login'),
    path(" ",include(router.urls)),

]
