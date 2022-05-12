import os
import django
import csv
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_prj.settings')
django.setup()

from main.models import car_list_test

with open('sample.csv', 'r', encoding='utf-8') as f:
    dr = csv.DictReader(f)
    s = pd.DataFrame(dr)
    
info = []
for i in range(len(s)):
    info.append(s.iloc[i,:])
    
for j in range(len(info)):
    car_list_test.objects.create(maker = info[j][0], car_list=info[j][1])