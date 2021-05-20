from django.urls import path, include
from .views import index_view,download_view
urlpatterns = [
    path('', index_view, name='index'),
    path('download/', download_view, name='donwload')
    
]
