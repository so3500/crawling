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


def get_query(sql, cursor, price):
    '''
    :param sql: 집계 값을 구하기 위한 select 쿼리
    :param cursor: 커서
    :param price: 가격 기준
    :return: 각각의 집계 값, AVG(*), MAX(*), MIN(*), STD(*)
    '''
    cursor.execute(sql, price)
    for row in cursor:
        return int(row['AVG(diff_product_price)']), row['MAX(diff_product_price)'],\
               row['MIN(diff_product_price)'], int(row['STD(diff_product_price)'])

'''
가격이 변한 제품 중
    가격이 오른 제품의 평균, 최대값, 최소값, 표준편차
    가격이 내려간 제품의 평균, 최대값, 최소값, 표준편차
'''
# diff_price_plus_avg = 0
# diff_price_plus_max = 0
# diff_price_plus_min = 0
# diff_price_plus_std = 0
diff_price_minus_avg = 0
diff_price_minus_max = 0
diff_price_minus_min = 0
diff_price_minus_std = 0

n_groups = 4

cursor = connection.cursor()

# sql = '''SELECT AVG(diff_product_price), STD(diff_product_price),
#                 MAX(diff_product_price), MIN(diff_product_price)
#          FROM product_0526
#          WHERE diff_product_price>%s;'''
# diff_price_plus_avg, diff_price_plus_max, diff_price_plus_min, diff_price_plus_std = get_query(sql, cursor, 0)

sql = '''SELECT AVG(diff_product_price), STD(diff_product_price), 
                MAX(diff_product_price), MIN(diff_product_price) 
         FROM product_0526 
         WHERE diff_product_price<%s;'''
diff_price_minus_avg, diff_price_minus_max, diff_price_minus_min, diff_price_minus_std = get_query(sql, cursor, -1)

'''
diff_price_plus_* : 올라간 가격의 평균, 표준편차, 최대, 최소
diff_price_minus_*: 내려간 가격의 평균, 표준편차, 최대, 최소
'''

price_info = (diff_price_minus_avg, diff_price_minus_max, diff_price_minus_min, diff_price_minus_std)

fig, ax = plt.subplots()

n_groups = 4
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, price_info, bar_width,
                 alpha=opacity,
                 color='r',
                 # yerr=std_men,
                 error_kw=error_config,
                 label='price_0526')

plt.xlabel('price_group')
plt.ylabel('number of product')
plt.title('product price info')

x_axis = ('minus_avg : {} '.format(diff_price_minus_avg),
          'minus_max : {} '.format(diff_price_minus_max),
          'minus_min : {} '.format(diff_price_minus_min),
          'minus_std : {} '.format(diff_price_minus_std))

# 왼쪽부터 가격변동이 없는 제품의 수, 현재 가격이 표시 되어있지않은 제품의 수, 가격이 오른 제품의 수, 가격이 내려간 제품의 수
plt.xticks(index + bar_width / 2,
           x_axis)
plt.legend()

plt.tight_layout()
plt.show()

connection.close()