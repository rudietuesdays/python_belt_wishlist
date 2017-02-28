#### WISH LIST URLS ####
from django.conf.urls import url
from . import views

app_name = 'wishList'
urlpatterns = [
    url(r'^$', views.index, name ='dashboard'),
    url(r'^wish_items$', views.add_item, name ='add'),
    url(r'^create$', views.create_item, name ='create'),
    url(r'^wish_items/(?P<id>\d+)$', views.view_item, name ='view'),
    url(r'^delete/(?P<id>\d+)$', views.delete_item, name ='delete'),
    url(r'^add_to_wishlist/(?P<id>\d+)$', views.join_item, name ='join'),
        url(r'^remove/(?P<id>\d+)$', views.remove_item, name ='remove'),

]
