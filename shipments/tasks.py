import logging
from BolSellerApp.celery import app
from ratelimit import limits, sleep_and_retry
from seller_profile.models import SellerProfile
from shipments.models import ShippingDetails, OrderDetails, TransportDetails, CustomerDetails, BillingDetails
from django.shortcuts import get_object_or_404
from django.http.request import QueryDict
from .serializers import *
import json
import requests

logger = logging.getLogger(__name__)

ONE_MINUTE = 60
@sleep_and_retry
@limits(calls=14, period=ONE_MINUTE)
def shipment_details_api(headers, url, payload):
    response = requests.request("GET", url, headers=headers, data=payload)
    return response


def get_new_access_token(seller_profile):
    seller_profile = get_object_or_404(SellerProfile, id=seller_profile)
    url = "https://login.bol.com/token?grant_type=client_credentials"
    payload = {'client_id': seller_profile.client_id,
               'client_secret': seller_profile.client_secret,
               'grant_type': 'client_credentials'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        res_data = response.json()
        new_access_token = res_data["access_token"]
        # Update the seller account with new access token
        get_seller_profile = get_object_or_404(SellerProfile, id=seller_profile.id)
        get_seller_profile.access_token = new_access_token
        get_seller_profile.save()
        return new_access_token


@app.task
def save_shipment_details_to_db(shipment_data, seller_profile, access_token):
    logger.debug('shipment data', shipment_data)
    logger.debug('seller profile', seller_profile)
    logger.debug('Access token', access_token)
    for each_shipment in shipment_data['shipments']:
        shipmentId = str(each_shipment['shipmentId'])
        url = "https://api.bol.com/retailer/shipments/"+str(shipmentId)
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.retailer.v3+json',
            'Authorization': 'Bearer '+ access_token
        }
        shipment_details_response = shipment_details_api(headers, url, payload)
        res_data = shipment_details_response.json()
        if shipment_details_response.status_code == 200:
            # save in shipping details
            try:
                shipping_details = ShippingDetails()
                shipping_details.seller_profile_id = seller_profile
                shipping_details.shipmentId = res_data['shipmentId']
                shipping_details.shipmentDate = res_data['shipmentDate']
                try:
                    shipping_details.shipmentReference = res_data['shipmentReference']
                except:
                    shipping_details.shipmentReference = ""
                shipping_details.pickUpPoint = res_data['pickUpPoint']
                shipping_details.save()
                logger.debug('Shipping Details saved successfully')
                if res_data['transport']:
                    transport_details_dict = QueryDict.dict(res_data['transport'])
                    transport_serializer = TransportDetailsCreateSerializer(data=transport_details_dict)
                    if transport_serializer.is_valid():
                        transport_serializer.save()
                        shipping_details.transportDetails_id = transport_serializer.data['id']
                        shipping_details.save()
                        logger.debug('Transport details saved successfully in shipping details')
                if res_data['customerDetails']:
                    customer_details_dict = QueryDict.dict(res_data['customerDetails'])
                    customer_serializer = CustomerDetailsCreateSerializer(data=customer_details_dict)
                    if customer_serializer.is_valid():
                        customer_serializer.save()
                        shipping_details.customerDetails_id = customer_serializer.data['id']
                        shipping_details.save()
                        logger.debug('Customers details saved successfully in shipping details')
                if res_data["shipmentItems"]:
                    for each_order in res_data["shipmentItems"]:
                        order_details_dict = QueryDict.dict(each_order)
                        order_serializer = OrderDetailsCreateSerializer(data=order_details_dict)
                        if order_serializer.is_valid():
                            order_serializer.save()
                            shipping_details.orderDetails.add(order_serializer.data['id'])
                            shipping_details.save()
                try:
                    if res_data['billingDetails']:
                        billing_details_dict = QueryDict.dict(res_data['billingDetails'])
                        billing_serializer = BillingDetailsCreateSerializer(data=billing_details_dict)
                        if billing_serializer.is_valid():
                            billing_serializer.save()
                            shipping_details.billingDetails_id = billing_serializer.data['id']
                            shipping_details.save()
                            logger.debug('Billing details saved successfully in shipping details')
                except:
                    pass
            except:
                logger.debug('Shipping ID already Exists')
        elif shipment_details_response.status_code == 401 and res_data['title'] == 'Expired JWT':
            access_token = get_new_access_token(seller_profile)

    return