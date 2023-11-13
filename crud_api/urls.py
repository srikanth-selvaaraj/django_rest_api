from django.urls import path
from . import views

urlpatterns = [
    path('list_blogs', views.list_blogs, name='list_blogs'),
    path('create_blog', views.create_blog, name='create_blog'),
    path('update_blog/<int:pk>', views.update_blog, name='update_blog'),
    path('delete_blog/<int:pk>', views.delete_blog, name='delete_blog'),
]
