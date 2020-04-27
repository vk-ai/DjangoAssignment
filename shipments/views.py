from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, exceptions
from rest_framework.views import APIView
from .models import *
from .serializers import *
from helpers.response import *
from seller_profile.models import SellerProfile
import requests

# Create your views here.
class InitialSyncShipment(APIView):
    def get(self, request, pk):
        if pk:
            seller_profile = get_object_or_404(SellerProfile, id=pk)
            fulfillment_methods = ['FBR', 'FBB']
            for each_method in fulfillment_methods:
                get_shipments(each_method, seller_profile, seller_profile.access_token)
            return Response(format_response(success_message(successfully_synced)))
        else:
            return Response(format_response(error_message(invalid_seller_id), status.HTTP_400_BAD_REQUEST),
                            status=status.HTTP_400_BAD_REQUEST)


class ListShipmentsAPI(APIView):
    def get(self, request, pk):
        if pk:
            objs = ShippingDetails.objects.filter(seller_profile_id=pk)
            serializers = ShippingDetailsListSerializer(objs, many=True)
            return Response(format_response(serializers.data))
        else:
            return Response(format_response(error_message(invalid_seller_id), status.HTTP_400_BAD_REQUEST),
                            status=status.HTTP_400_BAD_REQUEST)
