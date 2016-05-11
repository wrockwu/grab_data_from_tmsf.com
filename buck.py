import os
import sys
import pickle
import array
import time as _time
import numpy as np
import pylab as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter

tmsf_file = os.path.expanduser('~/tmsf/price.txt')

ax = plt.gca()

def draw(x_time, y_price, an_area):
    ymajorLocator   = MultipleLocator(2500)
    yminorLocator   = MultipleLocator(500)

    width = 0.1
    idx = np.arange(len(x_time))
    plt.bar(idx, y_price, width, color='red', label='+++++++++++')
    plt.xticks(idx+width/2, x_time, rotation=90)
    plt.ylim(15000)
    plt.xlabel('time')
    plt.ylabel('price')
    plt.grid()
    plt.subplots_adjust(bottom=0.2)

    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_minor_locator(yminorLocator)
    ax.yaxis.grid(True, which='minor')

    for c in range(0, len(y_price)):
        ax.annotate(str(y_price[c]) + '(' + str(an_area[c]) + ')', xy=(c,y_price[c]), xycoords='data',
                                xytext=(1, 25), textcoords='offset points',
                                                arrowprops=dict(arrowstyle="->")
                                                                )

    plt.show()

if __name__ == '__main__':
    tm = _time.ctime()
    tm_list = tm.split(' ')
    last_count = 0
    last_area = 0
    last_price = 0
    last_total = 0
    last_len = 0
    last_day = 0
    x_time = []
    y_price = []
    an_area = []

    if not os.path.exists(tmsf_file):
        print('no data file')
        sys.exit(0)
    while True:
        with open(tmsf_file, 'rb') as datafile:
            a_list = pickle.load(datafile)
            length = len(a_list)
            print(a_list)

            if length == last_len:
                print('data unchange')
            else:
                for item in a_list:
                    tm_tag = item[0]
                    day = tm_tag[0:6]
                    print(day)
                    count = float(item[1])
                    area = float(item[3])
                    price = float(item[4])

                    if day == last_day:
                        pcs_count = count - last_count
                        pcs_area = round(area - last_area, 2)
                        pcs_price = round(((area*price) - last_total)/ pcs_area, 2)
                        last_count = count
                        last_area = area
                        last_total = area * price
                        last_day = day
                        x_time.append(item[0])
                        y_price.append(pcs_price)
                        an_area.append(pcs_area)
                    else:
                        print('new day ' + day)
                        last_count = 0
                        last_area = 0
                        last_total = 0

                        pcs_count = count - last_count
                        pcs_area = round(area - last_area, 1)
                        pcs_price = round(((area*price) - last_total)/ pcs_area, 1)
                        last_count = count
                        last_area = area
                        last_total = area * price
                        last_day = day
                        x_time.append(item[0])
                        y_price.append(pcs_price)
                        an_area.append(pcs_area)

                    print(pcs_count,pcs_area,pcs_price)
        draw(x_time, y_price, an_area)
        _time.sleep(10)
