import os
import django
import csv
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_prj.settings')
django.setup()

from main.models import maker_test

with open('test.csv', 'r', encoding='utf-8') as f:
    dr = csv.DictReader(f)
    s = pd.DataFrame(dr)
    
info = []
for i in range(len(s)):
    info.append(s.iloc[i,:])
    
for j in range(len(info)):
    maker_test.objects.create(maker = info[j][0])