"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from socialnetwork import views as social_views

urlpatterns = [
    url(r'^login$',auth_views.login,{'template_name':'login_form.html'},name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$',social_views.register,name='register'),
    url(r'^profile/(?P<user_id>\d+)$',social_views.profile,name='profile'),
    url(r'^addPost$',social_views.add_post,name='addPost'),
    url(r'^editProfile$',social_views.edit_profile,name='editProfile'),
    url(r'^follow/(?P<id>\d+)$',social_views.follow,name='follow'),
    url(r'^unfollow/(?P<id>\d+)$',social_views.unfollow,name='unfollow'),
    url(r'^followees$',social_views.followees,name='followee'),
    url(r'^getAvatar/(?P<id>\d+)',social_views.get_avatar,name='getAvatar'),
    url(r'^getPostAfter',social_views.get_post_after),
    url(r'^addReply',social_views.add_reply),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        social_views.confirm_registration, name='confirm'),
    url(r'^$',social_views.home,name='home')
]
