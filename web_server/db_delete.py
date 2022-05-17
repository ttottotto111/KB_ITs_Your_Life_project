import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_prj.settings')
django.setup()

from main.models import car_list

car_list.objects.all().delete()