from django.contrib import admin
from django.urls import path, include, re_path
from apirest.views import TripViewSet
from rest_framework import routers

# define the router

urlpatterns = [
    path('trips/allTrips', TripViewSet.as_view({'get': 'list'})),
    path('trips/insert', TripViewSet.as_view({'post': 'insert'})),
    re_path(r'^trips/queryByRegion/(?P<region>[A-Z][a-z]+\w+)/$', TripViewSet.as_view({'get': 'queryByRegion'})),
    re_path(r'^trips/queryByCoordinates/(?P<longitud>[0-9]{1,2}\.[0-9]+\d+)/(?P<latitud>[0-9]{1,2}\.[0-9]+\d+)/$', TripViewSet.as_view({'get': 'queryByCoordinates'})),
]