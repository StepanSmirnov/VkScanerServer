from django.conf.urls import url

from . import views

app_name = 'scanner'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^scan/$', views.create, name='scan'),
    url(r'^ajax/scan_photo/$', views.scanPhoto, name='scan_photo'),
    url(r'^ajax/make_chart/$', views.makeChart, name='make_chart'),
]