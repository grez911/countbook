from django.conf.urls import url
from django.views.generic.base import TemplateView

#from . import views

app_name = 'website'
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^append_operation/$', views.append_operation, name='append_operation'),
]
