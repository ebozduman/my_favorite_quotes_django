from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_process$', views.register_process),
    url(r'^login_process$', views.login_process),
    url(r'^show_home$', views.show_home),
    url(r'^add_quote$', views.add_quote),
    url(r'^poster_favorites/(?P<poster_id>\d+)$', views.show_poster_favorites),
    url(r'^add_to_my_favorites$', views.add_show_my_favorites),
    url(r'^remove_from_my_list$', views.remove_from_my_list),
    url(r'^logout$', views.logout),
]
