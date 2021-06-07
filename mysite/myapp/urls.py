from django.urls import path, include
from .views import index_view,download_view, week_view
urlpatterns = [
    path('', index_view, name='index'),
    path('download/', download_view, name='donwload'),
    path('week/', week_view, name='week', kwargs={'collection_name': ''}),
    path('week/<str:collection_name>', week_view, name='week'),
    
]
