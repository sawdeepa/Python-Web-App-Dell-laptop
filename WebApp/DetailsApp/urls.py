
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url
from . import views
from .views import MasterListView

#TEMPLATE TAGGING
app_name='DetailsApp'


urlpatterns = [

    path('<int:id>/', views.tilesid,name='Tilesid'),
    path('refresh/<str:DomainID>/<str:id>', views.refresh,name='refresh'),
    path('details/<int:id>', views.details,name='Details'),
    path('details/<int:id>/download_zip', views.send_file,name='Download'),
    path('error/', views.error,name='error'),
    #path('refresh/<int:id>/<str:strid>', views.refresh,name='Refresh'),
    #path('<int:RID>/<int:CATID>', views.fetch,name='Insight'),
    #url(r'^$',views.MasterDetailView.as_view(),name='list'),
    #url(r'^(?P<pk>\d+)/$',views.MasterDetailView.as_view(),name='detaillist'),
    path('',views.index,name='index'),
]
