from seller_profile.models import SellerProfile
from django.shortcuts import get_object_or_404
from ratelimit import limits, sleep_and_retry
from shipments.tasks import save_shipment_details_to_db
import requests
import json

'''Response Messages'''
deleted_successfully = 'Deleted Successfully'
invalid_client_id = 'Invalid Client ID and Client Secret'
invalid_seller_id = 'Invalid Seller ID'
successfully_synced = 'Successfully Synced'


'''Helper function for formatting response'''
def format_response(data, status=200):
    context = {
        'statusCode': status,
        'data': data
    }
    return context

'''Custom error message display from serializer'''
def custom_error(error_data):
    for key in error_data:
        key_name = key.replace('_', ' ').capitalize()
        return {"message": error_data[key][0].replace('This', key_name).rstrip('.')}
    return None

'''Success message display'''
def success_message(message_variable, start_custom_message = '', end_custom_message = ''):
    return {"message": message_variable}


'''Error message display'''
def error_message(message_variable, start_custom_message = '', end_custom_message = ''):
    return {"message": message_variable}


'''Helper function to get new access token once expired'''
def get_new_access_token(seller_profile):
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


'''Healper function to call shipment API with rate limit'''
ONE_MINUTE = 60
@sleep_and_retry
@limits(calls=7, period=ONE_MINUTE)
def shipment_api(headers, url, payload):
    response = requests.request("GET", url, headers=headers, data=payload)
    return response


'''Helper function to call Shipment API'''
def get_shipments(method, seller_profile, access_token):
    page_num = 1
    payload = {}
    while True:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.retailer.v3+json',
            'Authorization': 'Bearer ' + access_token
        }
        url = "https://api.bol.com/retailer/shipments?fulfilment-method="+method+"&page="+str(page_num)
        shipment_response = shipment_api(headers, url, payload)
        res_data = shipment_response.json()
        if shipment_response.status_code == 200 and res_data != {}:
            # get_shipments_details(res_data, seller_profile)
            # json_data = json.dumps(res_data)
            save_shipment_details_to_db.delay(res_data, seller_profile.id, access_token)
            page_num += 1
        elif shipment_response.status_code == 401 and res_data['title'] == 'Expired JWT':
            access_token = get_new_access_token(seller_profile)
        else:
            break
    return
