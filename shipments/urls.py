from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^initial-sync-shipment(/(?P<pk>\d+))*/$', InitialSyncShipment.as_view()),
    url(r'^list-all-shipments(/(?P<pk>\d+))*/$', ListShipmentsAPI.as_view()),
    ]