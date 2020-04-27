import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BolSellerApp.settings')

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('BolSellerApp')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()