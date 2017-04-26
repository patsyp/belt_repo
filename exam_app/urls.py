from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index),
	url(r'^register$', views.createUser),
	url(r'^login$', views.login),
	url(r'^success$', views.success),
	url(r'^logout$', views.logout),
	url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
	url(r'^users/profile/(?P<id>\d+)$', views.show_profile),
	url(r'^delete_friend/(?P<id>\d+)$',views.delete_friend),
	]