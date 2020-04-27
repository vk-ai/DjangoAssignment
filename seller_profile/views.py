from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, exceptions
from rest_framework.views import APIView
from .models import *
from .serializers import *
from helpers.response import *
import requests


# Create your views here.
class SellerProfileAPI(APIView):
    '''
    class to create, update, list and delete Seller Profile
    '''
    def get(self, request, pk=None):
        if pk is not None:
            obj = get_object_or_404(SellerProfile, id=pk)
            serializer = SellerProfileListSerializer(obj)
        else:
            objs = SellerProfile.objects.all()
            serializer = SellerProfileListSerializer(objs, many=True)
        return Response(format_response(serializer.data))

    def post(self, request):
        query_dict = QueryDict.dict(request.data)
        url = "https://login.bol.com/token?grant_type=client_credentials"
        payload = {'client_id': query_dict['client_id'],
                   'client_secret': query_dict['client_secret'],
                   'grant_type': 'client_credentials'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            res_data = response.json()
            query_dict['access_token'] = res_data["access_token"]
            serializer = SellerProfileCreateSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save()
                return Response(format_response(serializer.data, status.HTTP_201_CREATED),
                                status=status.HTTP_201_CREATED)
            return Response(format_response(custom_error(serializer.errors), status.HTTP_400_BAD_REQUEST),
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(format_response(error_message(invalid_client_id), status.HTTP_400_BAD_REQUEST),
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        seller_profile = get_object_or_404(SellerProfile, id=pk)
        serializer = SellerProfileCreateSerializer(seller_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(format_response(serializer.data, status.HTTP_201_CREATED),
                            status=status.HTTP_201_CREATED)
        return Response(format_response(custom_error(serializer.errors), status.HTTP_400_BAD_REQUEST),
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        seller_profile = get_object_or_404(SellerProfile, id=pk)
        seller_profile.delete()
        return Response(format_response(success_message(deleted_successfully)))