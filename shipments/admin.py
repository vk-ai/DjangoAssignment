from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ShippingDetails)
admin.site.register(TransportDetails)
admin.site.register(CustomerDetails)
admin.site.register(OrderDetails)
admin.site.register(BillingDetails)