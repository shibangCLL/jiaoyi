from django.urls import re_path, path
from . import views

app_name = 'jiaoyi'

urlpatterns = [
    re_path(r'^addproduct/$', views.addproduct, name='addproduct'),
    re_path(r'^user/mylisting/$', views.mylisting, name='mylisting'),
    re_path(r'^user/listing/$', views.listing, name='listing'),
    re_path(r'^user/product/(?P<pk>\d+)/$', views.pro_detail, name='pro_detail'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),

    # re_path(r'^user/pic/(?P<pk>\d+)/$', views.pic_detail, name='pic_detail'),
]
