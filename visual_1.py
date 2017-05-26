import csv
import logging
import re
from urllib.request import urlopen

import pymysql.cursors
import pymysql
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=' ',
                             db='sys',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_query(sql, cursor, price):
    '''
    :param sql: 집계 값을 구하기 위한 select 쿼리
    :param cursor: 커서
    :param price: 가격 기준
    :return: 집계 값
    '''
    cursor.execute(sql, price)
    for row in cursor:
        print(row['COUNT(*)'])
        return row['COUNT(*)']

diff_price_zero = 0
real_price_no = 0
diff_price_plus = 0
diff_price_minus = 0

n_groups = 4

cursor = connection.cursor()

sql = 'SELECT COUNT(*) FROM product_0526 WHERE diff_product_price=%s'
diff_price_zero = get_query(sql, cursor, 0)
sql = 'SELECT COUNT(*) FROM product_0526 WHERE real_product_price=%s'
real_price_no = get_query(sql, cursor, -1)
sql = 'SELECT COUNT(*) FROM product_0526 WHERE diff_product_price>%s'
diff_price_plus = get_query(sql, cursor, 0)
sql = 'SELECT COUNT(*) FROM product_0526 WHERE diff_product_price<%s'
diff_price_minus = get_query(sql, cursor, -1)

price_info = (diff_price_zero, real_price_no, diff_price_plus, diff_price_minus)
fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, price_info, bar_width,
                 alpha=opacity,
                 color='b',
                 # yerr=std_men,
                 error_kw=error_config,
                 label='price_0526')

plt.xlabel('price_group')
plt.ylabel('number of product')
plt.title('product price info')

x_axis = ('no_fluctuation : {} '.format(diff_price_zero),
          'no_price : {} '.format(real_price_no),
          'plus_fluctuation : {} '.format(diff_price_plus),
          'minus_fluctuation : {} '.format(diff_price_minus))

# 왼쪽부터 가격변동이 없는 제품의 수, 현재 가격이 표시 되어있지않은 제품의 수, 가격이 오른 제품의 수, 가격이 내려간 제품의 수
plt.xticks(index + bar_width / 2,
           x_axis)
plt.legend()

plt.tight_layout()
plt.show()

connection.close()