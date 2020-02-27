from django.urls import include, path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('visualization/',views.visualization,name='visualization'),
    path('visualization/to_split_data',views.to_split_data,name='to_split_data'),
    path('visualuzation/split_data',views.split_data,name='split_data'),
    path('visualization/data',views.data,name='data'),
    path('visualization/X_train/',views.X_train,name='X_train'),
    path('visualization/X_test/',views.X_test,name='X_test'),
    path('visualization/y_train/',views.y_train,name='y_train'),
    path('visualization/y_test/',views.y_test,name='y_test'),
    path('visualization/stock/',views.stock,name='stock'),
    path('visualization/Prediction',views.prediction,name='prediction'),
    path('visualization/predict/',views.predict,name='predict'),
    path('visualization/Pct_Matrix',views.to_PctMatrix,name="PctMatrix"),
    path('visualization/MVND/',views.MVND,name='MVND'),
]