from django.conf.urls import url
from . import views

app_name='spiders'

urlpatterns=[
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
    url(r'^login/$',views.log_in,name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$',views.log_out,name='logout'),
    url(r'^post/(?P<pk>[0-9]+)/comment/$',views.comment,name='comment')
]