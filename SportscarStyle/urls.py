"""SportscarStyle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('User.urls', namespace='account')),
    url(r'^cars/', include('Sportscar.urls', namespace='cars')),
    url(r'^news/', include('News.urls', namespace='news')),
    url(r'^status/', include('Status.urls', namespace='status')),
    url(r'^settings/', include('SettingCenter.urls', namespace='settings')),
    url(r'^activity/', include('Activity.urls', namespace='activity')),
    url(r'^notification/', include('Notification.urls', namespace="notification")),
    url(r'^radar/', include('Location.urls', namespace="radar")),
    url(r'^club/', include('Club.urls', namespace='club')),
    url(r'^chat/', include('Chat.urls', namespace='chat'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
