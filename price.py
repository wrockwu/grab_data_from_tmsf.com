import time as _time
from datetime import date, time, timezone, datetime, timedelta
import os
import pickle
import urllib.request
import re
from bs4 import BeautifulSoup

url = 'http://www.tmsf.com/daily.htm'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent':user_agent}
user_href = "/newhouse/property_33_169276739_info.htm"
file_path = '/home/bwu/tmsf_price.txt'
regular_letter = '.*?class="numb(.*?)"'
dic_let2arb={'zero':'0','one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','dor':'.'}

h_start = 9
h_end = 23
s_sleep = 30*60

def cut_down(s_data, u_href):
    soup = BeautifulSoup(s_data, 'lxml')
    '''first, get all main district data by node 'div' & style='display:block' '''
    all_main_data = soup.find('div', style = 'display:block')
    '''second, find target son data by node 'a' & href(is a url,
    modify this condition later version)'''
    target_raw_data = all_main_data.contents[1].find_next('a', href = u_href)
    '''last, find & return parent 'tr' node, include all raw data'''
    return target_raw_data.find_previous('tr')

def pick_major(list_data):
    '''transform letter number to arbic number'''
    house_ripe = []
    for t in list_data:
        if len(t):
            if isinstance(t, list):
                res = ''
                for le in t:
                    res += (dic_let2arb[le])
                t = res
                house_ripe.append(t)
        else:
            continue
        
    return house_ripe

def extract_data(td_data):
    '''pick up major data'''
    primary_filter = []
    pattern = re.compile(regular_letter, re.S)
    for item in td_data:
        string = item.find_all('span')
        primary_filter.append(re.findall(pattern, str(string).strip()))

    return pick_major(primary_filter)
    
def web_data():
    '''scrab raw data from web'''
    req = urllib.request.Request(url, headers=headers)
    try:
        src_data =  urllib.request.urlopen(req).read()
    except urllib.error.URLError as e:
        print(e.reason)
    except urllib.error.HTTPError as e:
        print(e.reason())

    src_data = src_data.decode('utf-8')
    tr_data = cut_down(src_data, user_href)
    td_data = tr_data.find_all('td')
    
    return td_data

def main():
    '''extract data about signed count, area, price'''
    ripe = extract_data(web_data())

    '''store to file'''
    try:
        with open(file_path, 'at+') as data_file:
            print(ripe, file = data_file)
    except IOError as err:
        print('File Error:' + str(err))

    with open(file_path, 'r') as data_file:
        print(data_file.readlines())

if __name__ == '__main__':
    '''set timezone to PRC'''
    os.environ['TZ'] = 'PRC'
    _time.tzset()

    while True:
        h_now = _time.localtime().tm_hour
        min_now = _time.localtime().tm_min
        sec_now = _time.localtime().tm_sec
        t_sleep = s_sleep
        
        '''30min a cycle, calc left time should sleep'''
        if min_now > 30:
            min_now -= 30
        
        if (h_now > h_start) and (h_now < h_end):
            '''scrab data every 30min in this period'''
            main()
            t_sleep = s_sleep - ((min_now)*60 + sec_now)
            _time.sleep(t_sleep)
        else:
            '''sleep midnight'''
            t_sleep = s_sleep - ((min_now)*60 + sec_now)
            print('time now: ' + str(_time.ctime()))
            print('we will sleep ' + str(t_sleep) + 's')
            _time.sleep(t_sleep)

