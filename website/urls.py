from django.conf.urls import url

from . import views

app_name = 'website'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^append_operation/$', views.append_operation, name='append_operation'),
]
