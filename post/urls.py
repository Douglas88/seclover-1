from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.IndexTemplateView.as_view(), name='index'),
    url(r'^posts/$', views.PostList.as_view(), name='posts'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='post_detail'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^register', views.register, name='register')
]
