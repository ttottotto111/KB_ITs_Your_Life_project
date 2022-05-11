import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_prj.settings')
django.setup()

from main.models import maker_test

f = open('test.csv', 'r', encoding='utf-8')
info = []

rdr = csv.reader(f)

for row in rdr:
    # make = row
    # tuple = (make)
    # info.append(tuple)
    maker_test.objects.create(maker = row)
f.close()

# ma = []
# for m in info:
    #ma.append(maker_test(maker = m))
    #maker_test.objects.create(maker = m)