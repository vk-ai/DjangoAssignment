from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^seller-profile(/(?P<pk>\d+))*/$', SellerProfileAPI.as_view()),
    ]