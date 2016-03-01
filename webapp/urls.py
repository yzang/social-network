from django.conf.urls import include, url

from hello import views as helloView
from socialnetwork import views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url('^socialnetwork/',include('socialnetwork.urls')),
    url(r'^db', helloView.db, name='db'),
    url('^$',views.home),
]
