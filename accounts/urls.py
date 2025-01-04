from django.urls import path
from .import views
from .views import  *

urlpatterns = [
    path('',views.userRegistration,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logout_view,name='logout'),
]
