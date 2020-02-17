from django.urls import include, path
from . import views

urlpatterns = [
    path('visualization/',views.visualization,name='visualization')
]