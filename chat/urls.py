from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from .views import Home


urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path("chat/",Home.as_view())
   
]