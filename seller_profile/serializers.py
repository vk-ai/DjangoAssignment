from rest_framework import serializers
from .models import *

class SellerProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = '__all__'


class SellerProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = '__all__'