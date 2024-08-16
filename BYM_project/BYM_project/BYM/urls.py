"""BYM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from main_app.views import SearchDishApi, ChangeCartApi, ParseProductsApi, LoadDishDataApi,\
                           RegisterApi, LoadProductsApi, SyncCartApi, LoadLastAddressApi, SetLastAddressApi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('searchDishApi/', SearchDishApi.as_view()),
    path('changeCartApi/', ChangeCartApi.as_view()),
    path('parseProductsApi/', ParseProductsApi.as_view()),
    path('loadDishDataApi/', LoadDishDataApi.as_view()),
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('registerApi/', RegisterApi.as_view()),
    path('loadProductsApi/', LoadProductsApi.as_view()),
    path('syncCartApi/', SyncCartApi.as_view()),
    path('setLastAddressApi/', SetLastAddressApi.as_view()),
    path('loadLastAddressApi/', LoadLastAddressApi.as_view()),
]
