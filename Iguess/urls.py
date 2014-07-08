from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Iguess.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'main.views.login_view'),
    url(r'^register/$', 'main.views.register'),
    url(r'^index/$', 'main.views.index'),
    url(r'^logout/$', 'main.views.logout_view'),
    url(r'^choose/$', 'main.views.choose'),
    url(r'^rank/$','main.views.rank')
)
