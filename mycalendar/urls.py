"""mycalendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

from predictor.views import *
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('',include('django.contrib.auth.urls')),
    path('predictor/',include('predictor.urls')),
    url(r'^home/', home,name='home'),
    url(r'^come_again!/$',logout,name='logout'),
    url(r'^register/$',register,name='register'),
    url(r'^data/$',data,name='data'),
    

    path('regression', call_model.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
