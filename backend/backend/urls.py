from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from equipment.views import RegisterView  

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/register/", RegisterView.as_view(), name='register'),
    path("api/login/", obtain_auth_token, name='login'),            

    path("api/", include("equipment.urls")),
]