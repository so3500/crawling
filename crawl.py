import csv
import logging
import re
from urllib.request import urlopen

import pymysql.cursors
import pymysql
from bs4 import BeautifulSoup

logger = logging.getLogger("on_log")
logger.setLevel(logging.DEBUG)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=' ',
                             db='sys',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

connection_0526 = pymysql.connect(host='localhost',
                             user='root',
                             password=' ',
                             db='sys',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
def page_auction(bs_obj):
    '''
    :param bs_obj: 
    :return: real_price
    '''
    try:
        price_obj = bs_obj.find("", {"class": "price_real"}).span.previous_sibling
        real_price = price_obj
    except AttributeError:
        # 예외처리 : 실제 상품이 판매 종료되어 가격 정보를 얻을 수 없는 경우
        real_price = -1

    return real_price

def page_storefarm(bs_obj):
    '''
    :param bs_obj: 
    :return: real_price
    '''
    try:
        price_obj = bs_obj.find("", {"class": "fc_point sale"}).strong.span
        real_price = price_obj.get_text()
    except AttributeError:
        # 예외처리 : 실제 상품이 판매 종료되어 가격 정보를 얻을 수 없는 경우
        real_price = -1

    return real_price


def page_swindow(bs_obj):
    '''
    :param bs_obj: 
    :return: real_price
    '''
    try:
        price_obj = bs_obj.find("", {"class": "detail_name"}).strong.em
        real_price = price_obj.get_text()
    except AttributeError:
        # 예외처리 : 실제 상품이 판매 종료되어 가격 정보를 얻을 수 없는 경우
        real_price = -1

    return real_price

cnt = 0

# url 패턴 매칭에 사용할 변수
pattern_auction = 'http://pd.auction.co.kr/'
pattern_storefarm = 'http://storefarm.naver.com/'
pattern_swindow = 'http://swindow.naver.com/'
# 반복적인 매칭 작업에는 패턴을 미리 컴파일해서 시간단축 가능
# https://godoftyping.wordpress.com/2015/04/08/python-%EC%A0%95%EA%B7%9C%ED%91%9C%ED%98%84%EC%8B%9D/
re_auction = re.compile(pattern_auction)
re_storefarm = re.compile(pattern_storefarm)
re_swindow = re.compile(pattern_swindow)

mall = None
try:
    cursor_0526 = connection_0526.cursor()
    with connection.cursor() as cursor:
        select_sql = "SELECT product_url, product_price, id FROM product"
        cursor.execute(select_sql)
        for row in cursor:

            print("cnt : ", cnt)
            cnt += 1

            url = row['product_url']
            price = int(row['product_price'])
            origin_id = int(row['id'])
            site_index = -1
            real_price = 0

            # url이 어느 사이트에 속하는지 판단
            if re_storefarm.search(url) is not None:
                site_index = 0
            elif re_auction.search(url) is not None:
                site_index = 1
            elif re_swindow.search(url) is not None:
                site_index = 2

            # 목적 사이트가 아닌 url은 pass
            if site_index == -1:
                print("site_index is -1 ")
                continue

            # 호출
            page = urlopen(url)
            bs_obj = BeautifulSoup(page, 'html.parser')

            # site 별로 실제 가격(real_price)과 쇼핑몰 이름을 가져오는 함수 호출
            if site_index == 0:
                real_price = page_storefarm(bs_obj)
                mall = 'storefarm'
            elif site_index == 1:
                real_price = page_auction(bs_obj)
                mall = 'auction'
            elif site_index == 2:
                real_price = page_swindow(bs_obj)
                mall = 'swindow'

            if real_price == -1:
                print("real_price is -1 ")
                diff_price = -1
                insert_info = (origin_id, real_price, diff_price, mall)
            else:
                # 상품 가격을 인트형으로 변경
                real_price = int(real_price.replace(',', ''))
                diff_price = real_price - price

                insert_info = (origin_id, real_price, diff_price, mall)

            # Create a new record
            sql = """INSERT INTO `product_0526_`
                  (`origin_id`, `real_product_price`, `diff_product_price`, `mall`) 
                  VALUES (%s, %s, %s, %s)"""
            cursor_0526.execute(sql, insert_info)
            print("origin_id : {}, price : {}, real_price : {}, diff_price : {}, mall : {}"
                  .format(origin_id, price, real_price, diff_price, mall))

            # 쿼리 100개 마다 커밋
            if cnt % 100 == 0:
                connection_0526.commit()
        # 나머지 쿼리 커밋
        connection_0526.commit()
finally:
    cursor.close()
    cursor_0526.close()
    connection.close()