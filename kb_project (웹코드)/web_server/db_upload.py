import os
import django
import csv
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_prj.settings')
django.setup()

from main.models import car_list

with open('중고차데이터최종v12.csv', 'r', encoding='cp949') as f:
    dr = csv.DictReader(f)
    s = pd.DataFrame(dr)
    
info = []
for i in range(len(s)):
    info.append(s.iloc[i,:])
    
for j in range(len(info)):
     car_list.objects.create(company = info[j][3], name=info[j][4],name_detail = info[j][5],
                             price = info[j][6], boost=info[j][7],year = info[j][8],
                             color = info[j][9], km=info[j][10],change = info[j][11],
                             fure = info[j][12], find=info[j][13],still = info[j][14],
                             wheel = info[j][15], acc=info[j][16],distroy = info[j][17],
                             made = info[j][18], new_price=info[j][19],down_rate = info[j][20],
                             rate_year = info[j][21], rate_2023=info[j][22],rate_2024 = info[j][23],
                             rate_2025 = info[j][24], rate_2026=info[j][25],rate_2027 = info[j][26],
                             rate_2028 = info[j][27], rate_2029=info[j][28],rate_2030 = info[j][29],
                             present_down = info[j][30],down1 = info[j][31],down2 = info[j][32],
                             down3 = info[j][33],down4 = info[j][34],down5 = info[j][35], 
                             present_value = info[j][36],value1 = info[j][37],value2 = info[j][38],
                             value3 = info[j][39],value4 = info[j][40],value5 = info[j][41],
                             present_sub = info[j][42],sub1 = info[j][43],sub2 = info[j][44]
                             ,sub3 = info[j][45],sub4 = info[j][46],sub5 = info[j][47])