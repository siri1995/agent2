from django.conf.urls import url
from django.contrib.auth import views as auth_views
from tagent2 import views as tagent2_views
from . import views


urlpatterns = [
    url(r'^$', views.AgentList.as_view(), name='agent-list'),
    url(r'agent/add/$', views.AgentAddLocArefCreate.as_view(), name='agent-add'),
    url(r'agent/(?P<pk>[0-9]+)/$', views.AgentAddLocArefUpdate.as_view(), name='agent-update'),
    url(r'agent/(?P<pk>[0-9]+)/delete/$', views.AgentDelete.as_view(), name='agent-delete'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', tagent2_views.signup, name='signup'),
    url(r'login$', tagent2_views.agent_list, name='home'),
]