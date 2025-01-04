from django.urls import path
from .import views
from .views import  *

urlpatterns = [
    path('create/', TouristDestinationCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', TouristDestinationDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', TouristDestinationUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TouristDestinationDeleteView.as_view(), name='delete'),
    path('search/<str:place_name>/', TouristDestinationSearchView.as_view(), name='search'),  

    path('', views.index, name='destination_list'),
    path('tourist_create/', views.create_touristdestination, name='create_touristdestination'),
    path('tourist_view/<int:id>/', views.view_tourist_destination, name='fetch_tourist_destination'),
    path('tourist_tourist_update/<int:id>/', views.update_tourist_destination, name='update_tourist_destination'),
    path('tourist_delete/<int:id>/', views.delete_tourist_destination, name='delete_tourist_destination'),

]
