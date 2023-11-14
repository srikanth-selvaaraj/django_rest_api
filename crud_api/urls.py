from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('blogs', views.BlogList.as_view(), name='blogs'),
    path('blogs/<int:pk>', views.BlogActions.as_view(), name='blog_actions'),
    path('user/register', views.Register.as_view(), name='register'),
    path('user/login', views.Login.as_view(), name='login'),
    path('user/logout', views.Logout.as_view(), name='logout'),
]
