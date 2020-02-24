from django.urls import include, path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('visualization/',views.visualization,name='visualization'),
    path('visualization/X_train/',views.X_train,name='X_train'),
    path('visualization/X_test/',views.X_test,name='X_test'),
    path('visualization/y_train/',views.y_train,name='y_train'),
    path('visualization/y_test/',views.y_test,name='y_test'),
    path('visualization/stock/',views.stock,name='stock'),
    path('visualization/prediction/',views.prediction,name='prediction'),
    path('visualization/calculations/',views.calculations,name='calculations'),
]