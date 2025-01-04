from django.urls import path
from .import views
from .views import  *

urlpatterns = [
    path('', views.userview, name='userview'),
    path('view/<int:id>/', views.view, name='view'),

]
