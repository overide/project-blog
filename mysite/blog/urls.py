from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    # post views
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'tags/(?P<post_tag>[-\w]+)/$', views.PostListView.as_view(), name='post_list_by_tag'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})'\
        r'/(?P<post>[-\w]+)/$',
        views.PostDetailView.as_view(),
        name='post_detail'),

    url(r'^(?P<post_id>\d+)/share/$',
        views.PostShareView.as_view(),
        name='post_share'),
    url(r'^feeds/$', LatestPostsFeed(), name = 'post_feed'),

    # url(r'^$',views.post_list,name='post_list'),
    # url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})'\
    # 	r'/(?P<post>[-\w]+)/$',
    # 	views.post_detail,
    # 	name='post_detail'),
]
