#### LOGIN AND REGISTRATION URLS ####
from django.conf.urls import url
from . import views

app_name = 'loginReg'
urlpatterns = [
    url(r'^$', views.index, name ='index'),
    url(r'^register$', views.register_user, name = 'register'),
    url(r'^login', views.login_user, name = 'login'),
    url(r'^logout', views.logout_user, name = 'logout')
]
