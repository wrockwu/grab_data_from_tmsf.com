import os
import pickle
import array
import time as _time

tmsf_file = os.path.expanduser('~/tmsf/test.txt')

if __name__ == '__main__':

    if False:
        tmp_list = ['5', '2', '3', '4']
     #   tmp_list = ['++++']
        a_list = []  
        if os.path.getsize(tmsf_file) > 0:
            with open(tmsf_file, 'rb') as datafile:
                a_list = pickle.load(datafile)
                print(a_list)
                a_list.append(tmp_list)
                
            with open(tmsf_file, 'wb+') as datafile: 
                pickle.dump(a_list, datafile)
        else:
            with open(tmsf_file, 'wb+') as datafile:
                a_list.append(tmp_list)
                pickle.dump(a_list, datafile)


    if True:
        tm = _time.ctime()
        tm_list = tm.split(' ')
        print(tm_list)
        print(tm_list[3])
        with open(tmsf_file, 'rb') as datafile:
            a_list = pickle.load(datafile)
            for item in a_list:
                count = list[0]
                area = list[2]
                price = list[3]
