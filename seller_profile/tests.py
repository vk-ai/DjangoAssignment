# from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import SellerProfile
from .serializers import *

import json


class SellerProfileTests(APITestCase):
    def test_seller_profile(self):
        data = {"seller_name": "test_seller_profile", "client_id": "69bd83f1-1172-4b02-821a-b5a2af5a32da",
                "client_secret": "NfainCcmbafiCUiutV7IKmjn8NbOCbw6Xc16a-_MDVyC0jhfbekNIpQ3z3sNUHhNJJEhK3ORSbh8WWbf9zSGpQ"}
        response = self.client.post("/api/sellers/seller-profile/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SellerProfileListTests(APITestCase):
    def test_list_seller_profile(self):
        response = self.client.get("/api/sellers/seller-profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
