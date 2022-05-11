import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_prj.settings')
django.setup()

from main.models import maker_test

maker_test.objects.all().delete()