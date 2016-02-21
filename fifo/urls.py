from django.conf.urls import include, url
from django.contrib import admin
from errand.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'fifo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^services/$',services),
    url(r'pending/$', pending),
    url(r'^jobs$', jobs),
    url(r'administrator', administrator),
    url(r'log_out', log_out),
    url(r'getjobs', jobapi),
    url(r'getservices', serviceapi),
    url(r'grantservice', grantjobapi),
    url(r'acceptjob', acceptjobapi),
    url(r'addservice', addservice),
]
