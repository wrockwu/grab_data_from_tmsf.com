import time as _time
from datetime import date, time, timezone, datetime, timedelta
import os
import pickle
import urllib.request
import re
from bs4 import BeautifulSoup

tmsf_dir = os.path.expanduser('~/tmsf')
tmsf_file = os.path.expanduser('~/tmsf/price.txt')
tmsf_log = os.path.expanduser('~/tmsf/log.txt')

url = 'http://www.tmsf.com/daily.htm'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent':user_agent}
user_href = "/newhouse/property_33_169276739_info.htm"

regular_letter = '.*?class="numb(.*?)"'
dic_let2arb={'zero':'0','one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','dor':'.'}

tm_hour_start = 9
tm_hour_end = 23
freq = 2
tm_sec_sleep = freq*60

last_ripe = []

def debug(string):
    try:
        with open(tmsf_log, 'at+') as datafile:
            print(string, file=datafile)
    except IOError as err:
        print('IOError:' + err, file=datafile)

def cut_down(s_data, u_href):
    soup = BeautifulSoup(s_data, 'lxml')
    '''first, get all main district data by node 'div' & style='display:block' '''
    all_main_data = soup.find('div', style = 'display:block')
    '''second, find target son data by node 'a' & href(is a url,
    modify this condition later version)'''
    target_raw_data = all_main_data.contents[1].find_next('a', href = u_href)
    '''last, find & return parent 'tr' node, include all raw data'''
    if target_raw_data:
        return target_raw_data.find_previous('tr')
    '''non-exist specify data, return NULL'''
    debug('Zero Turnover')
    return target_raw_data

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
    '''scrab raw data from web, if network disconnect return NULL list to avoid exception'''
    td_data = []
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as src_data:
            src_data_dec = src_data.read().decode('utf-8')
    except urllib.error.URLError as e:
        debug(e.reason)
        return td_data
    except urllib.error.HTTPError as e:
        debug(e.reason)
        return td_data
    '''web don't have the specify data, return NULL td_data'''
    tr_data = cut_down(src_data_dec, user_href)
    if tr_data:
        td_data = tr_data.find_all('td')

    return td_data

def main():
    '''extract data about signed count, area, price'''
    ripe = extract_data(web_data())
    global last_ripe

    '''store to file'''
    try:
        with open(tmsf_file, 'at+') as data_file:
            '''store data if list has real data'''
            if ripe:
                if ripe == last_ripe:
                    debug("unchanged data:" + str(ripe) + ", ignore it")
                else:
                    debug("data changed:" + str(ripe))
                    print(ripe, file = data_file)
                    last_ripe = ripe
            else:
                debug('get data failed')
    except IOError as err:
        debug('File Error:' + str(err))

    print('last data is:' + str(last_ripe))

if __name__ == '__main__':
    '''creat data file&log file'''
    if not os.path.exists(tmsf_dir):
        os.mkdir(tmsf_dir)
    if not os.path.exists(tmsf_file):
        os.mknod(tmsf_file)
    if not os.path.exists(tmsf_log):
        os.mknod(tmsf_log)

    '''set timezone to PRC'''
    os.environ['TZ'] = 'PRC'
    _time.tzset()

    while True:
        tm_hour_now = _time.localtime().tm_hour
        tm_min_now = _time.localtime().tm_min
        tm_sec_now = _time.localtime().tm_sec
        tm_min = tm_min_now
        tm_need_sleep = tm_sec_sleep
        
        '''30min a cycle, calc left time should sleep'''
        while tm_min >= freq:
            tm_min -= freq
        
        if (tm_hour_now > tm_hour_start) and (tm_hour_now < tm_hour_end):
            '''scrab data every 30min in this period'''
            debug('picked up data @: ' + str(_time.ctime()))
            main()
            '''keep accurate to get second again, main() costs lot of time'''
            tm_sec_now = _time.localtime().tm_sec
            tm_need_sleep = tm_sec_sleep - ((tm_min)*60 + tm_sec_now)
            debug('sleep ' + str(tm_need_sleep) + 's')
            _time.sleep(tm_need_sleep)
        else:
            '''midnight wakeup every hour'''
            tm_need_sleep = 60*60 - ((tm_min_now)*60 + tm_sec_now)
            debug('+++++++++++++Rest Time+++++++++++++++++')
            debug('time: ' + str(_time.ctime()))
            debug('sleep ' + str(tm_need_sleep) + 's')
            _time.sleep(tm_need_sleep)

