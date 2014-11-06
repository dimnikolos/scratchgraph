from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import scratchgraph.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', scratchgraph.views.index, name='index'),
    url(r'^about',scratchgraph.views.about,name='about'),

)
