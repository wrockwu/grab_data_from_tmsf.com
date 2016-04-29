import os
import pickle
import array
import time as _time
import numpy as np
import pylab as pl

tmsf_file = os.path.expanduser('~/tmsf/price.txt')

if __name__ == '__main__':
    tm = _time.ctime()
    tm_list = tm.split(' ')
    last_count = 0
    last_area = 0
    last_price = 0
    last_total = 0
    last_len = 0
    x_time = []
    y_price = []

    print(_time.ctime())
    while True:
        with open(tmsf_file, 'rb') as datafile:
            a_list = pickle.load(datafile)
            length = len(a_list)
            print(a_list)

            if length == last_len:
                print('data unchange')
            else:
                for item in a_list:
                    count = float(item[1])
                    area = float(item[3])
                    price = float(item[4])

                    pcs_count = count - last_count
                    pcs_area = area - last_area
                    pcs_price = ((area*price) - last_total)/ pcs_area

                    last_count = count
                    last_area = area
                    last_total = area * price
                    last_len = length
                    x_time.append(item[0])
                    y_price.append(pcs_price)

                    print(pcs_count,pcs_area,pcs_price)

        width = 0.3
        idx = np.arange(len(x_time))
        pl.bar(idx, y_price, width, color='red', label='pcs price')
        pl.xticks(idx+width/2, x_time, rotation=360)
        pl.xlabel('time')
        pl.ylabel('price')
        pl.title('What The Fuck!')
        pl.show()
        _time.sleep(10)
