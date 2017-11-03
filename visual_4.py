import pymysql
import matplotlib.pyplot as plt
plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np


connection = pymysql.connect(host='localhost',
                             user='root',
                             password=' ',
                             db='sys',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
sql = """SELECT COUNT(*), mall
         FROM product_0526_
         WHERE (diff_product_price<-1 OR diff_product_price>0)
         GROUP BY mall;"""
cursor.execute(sql)

diff_num_storefarm = 0
diff_num_auction = 0
diff_num_swindow = 0

for row in cursor:
    print(row['mall'])
    if row['mall'] == 'storefarm':
        diff_num_storefarm = row['COUNT(*)']
    elif row['mall'] == 'auction':
        diff_num_auction = row['COUNT(*)']
    elif row['mall'] == 'swindpw':
        diff_num_swindow = row['COUNT(*)']

total_diff = diff_num_storefarm + diff_num_auction + diff_num_swindow
ratio_storefarm =  diff_num_storefarm / total_diff
ratio_auction = diff_num_auction / total_diff
ratio_swindow = diff_num_swindow / total_diff
'''
diff_num_storefarm : storefarm 의 상품가격 변경 건 수 
diff_num_action    : action 의 상품가격 변경 건 수 
diff_num_swindow   : swindow 의 상품가격 변경 건 수 
'''

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'storefarm', 'auction', 'swindow'
sizes = [ratio_storefarm, ratio_auction, ratio_swindow]   # 각 쇼핑몰의 가격 변경 건수 비중
explode = (0.1, 0.1, 0.1)  # 가운데 점에서 퍼지는 정도

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

connection.close()