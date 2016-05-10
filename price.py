import time as _time
from datetime import date, time, timezone, datetime, timedelta
import os
import sys
import pickle
import urllib.request
import re
from bs4 import BeautifulSoup

'''debug information output on/off'''
DEBUG_OUTPUT = 'ON'

url = 'http://www.tmsf.com/daily.htm'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent':user_agent}
user_href = '盛世诚品公寓'

tmsf_dir = os.path.expanduser('~/tmsf')
tmsf_file = os.path.expanduser('~/tmsf/price.txt')
tmsf_log = os.path.expanduser('~/tmsf/log.txt')

regular_letter = '.*?class="numb(.*?)"'
letter2arb={'zero':'0','one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','dor':'.'}

'''put this tag in data list'''
tm_tag = '00:00:00'
'''work start time & end time'''
tm_hour_start = 9
tm_hour_end = 23
'''grab data frequency'''
freq = 1
tm_sec_sleep = freq*60
'''url open failed retry time'''
retry_times = 5

'''store last time's data'''
last_ripe = ['0', '0', '0', '0']

def debug(string):
    if DEBUG_OUTPUT == 'ON':
        try:
            with open(tmsf_log, 'at+') as datafile:
                print(string, file=datafile)
        except IOError as err:
            print('IOError:' + err, file=datafile)
    else:
        print(string)

def data_handler(s_data, u_href):
    data = []
    processed_data =[]
    complete_data = []

    if not s_data:
        debug('source data error')
        return complete_data

    soup = BeautifulSoup(s_data, 'lxml')
    '''get specify house information'''
    data = soup.find('div', style='display:block')
    if data == None:
        debug('#1 cant find data table(incomplete web data?)')
        data = []
        return data

    if data.table == None:
        debug('#2 cant find data table(incomplete web data?)')
        data = []
        return data
    data = data.table.find_all('a', href=True)
    for item in data:
        if(item.string == u_href):
            break
        else:
            item = None
    data = item
    if data == None :
        '''specify house isn't there, error court name or zero turnover?'''
        debug('wrong court name or zero turnover until now')
        data = []
        return data
    data = data.find_parent('tr')
    if data == None:
        debug('html style#1 changed, must modify rule immediately')
        data = []
        return data
    data = data.find_all('td')
    if not data:
        debug('html style#2 changed, must modify rule immediately')
        data = []
        return data

    '''seek key info from 'data' struct'''
    pattern = re.compile(regular_letter, re.S)
    for item in data:
        string = item.find_all('span')
        processed_data.append(re.findall(pattern, str(string).strip()))

    '''convert letters to arabic numerals'''
    complete_data = []
    complete_data.append(tm_tag)
    for t in processed_data:
        if len(t):
            if isinstance(t, list):
                res = ''
                for le in t:
                    res += (letter2arb[le])
                complete_data.append(res)
        else:
            continue

    return complete_data

def url_open():
    retry = 0
    req = urllib.request.Request(url, headers=headers)
    while retry < retry_times:
        retry += 1
        try:
            data = urllib.request.urlopen(req)
            if not (data == None):
                return data.read().decode('utf-8')
        except urllib.error.URLError as e:
            debug("retry times:" + str(retry))
            debug(e.reason)
            continue
        except urllib.error.HTTPError as e:
            debug("retry times:" + str(retry))
            debug(e.reason)
            continue
        except:
            debug('unknow except, retry times:' + str(retry))
            continue

    debug("url open failed")
    return False

def store2file(data):
    a_list = []
    if os.path.getsize(tmsf_file) > 0:
        with open(tmsf_file, 'rb') as datafile:
            a_list = pickle.load(datafile)
            a_list.append(data)
            debug(a_list)

        with open(tmsf_file, 'wb+') as datafile:
            pickle.dump(a_list, datafile)
    else:
        with open(tmsf_file, 'wb+') as datafile:
            a_list.append(data)
            pickle.dump(a_list, datafile)

def main():
    '''extract data about signed count, area, price'''
    ripe = data_handler(url_open(), user_href)
    global last_ripe

    '''store to file'''
    try:
        with open(tmsf_file, 'ab+') as data_file:
            '''store data if list has real data'''
            if ripe:
                '''[1] is count, count unchang, other info mustn't chang, ignore it'''
                if ripe[1] == last_ripe[1]:
                    debug('ignore unchanged data:' + str(ripe))
                else:
                    debug('store changed data:' + str(ripe))
                    store2file(ripe)
                    debug('store data success')
                    last_ripe = ripe
    except IOError as err:
        debug('File Error:' + str(err))

def get_last_data():
    global last_ripe

    if os.path.getsize(tmsf_file) > 0:
        with open(tmsf_file, 'rb') as datafile:
            a_list = pickle.load(datafile)
            last_ripe = a_list[-1]

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
    get_last_data()

    arg_list = sys.argv[1:]
    if not arg_list:
        print('No Specify Court Name, Use Default Court Name:' + user_href)
    if len(arg_list) > 1:
        print("Too Much Court, Only One A Time!!!")
        sys.exit(0)
    if len(arg_list) == 1:
        print("Full Court Name is:" + arg_list[0])
        user_href = arg_list[0]

    while True:
        tm_hour_now = _time.localtime().tm_hour
        tm_min_now = _time.localtime().tm_min
        tm_sec_now = _time.localtime().tm_sec
        tm_min = tm_min_now
        tm_need_sleep = tm_sec_sleep
        '''extract time, drop date'''
        tm_list = _time.ctime().split(' ')
        tm_tag = tm_list[1] + ' ' + tm_list[3] + ' ' + tm_list[4]

        '''calc left time should sleep'''
        while tm_min >= freq:
            tm_min -= freq

        if (tm_hour_now > tm_hour_start) and (tm_hour_now < tm_hour_end):
            '''scrab data every 1 min'''
            debug('start pick up data @ ' + tm_tag)
            main()
            '''keep accurate to get second again, main() costs lot of time'''
            tm_sec_now = _time.localtime().tm_sec
            tm_need_sleep = tm_sec_sleep - ((tm_min)*60 + tm_sec_now)
            debug('sleep ' + str(tm_need_sleep) + 's')
            _time.sleep(tm_need_sleep)
        else:
            '''midnighti, wakeup every hour'''
            tm_need_sleep = 60*60 - ((tm_min_now)*60 + tm_sec_now)
            debug('+++++++++++++Rest Time+++++++++++++++++')
            debug('time @ ' + tm_tag)
            debug('sleep ' + str(tm_need_sleep) + 's')
            _time.sleep(tm_need_sleep)

