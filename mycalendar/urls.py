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
from django.contrib.auth import views as auth_views
from events import views as user_views
# from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',  user_views.register, name='register'),
    path('', include('events.urls')),
    # path('login/',auth_views.LoginView.as_view(template_name='events/login.html',name='login')),
    # path('logout/',auth_views.LoginView.as_view(template_name='events/logout.html',name='logout'))
 
    # url(r'^$', user_views.home, name='home'),
    # url(r'^signup/$', user_views.signup, name='signup'),
    # url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    # url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    
]
