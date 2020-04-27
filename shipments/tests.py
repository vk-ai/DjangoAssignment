from rest_framework import status
from rest_framework.test import APITestCase

from .models import *
from .serializers import *

class ListShipmentsTest(APITestCase):
    def test_list_shipment_details(self):
        response = self.client.get("/api/shipments/list-all-shipments/6/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
