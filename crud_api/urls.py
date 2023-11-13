from django.urls import path
from . import views

urlpatterns = [
    path('blogs', views.BlogList.as_view(), name='blogs'),
    path('blogs/<int:pk>', views.BlogActions.as_view(), name='blog_actions'),
]
