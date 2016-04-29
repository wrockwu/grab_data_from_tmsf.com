import os
import pickle
import array
import time as _time

tmsf_file = os.path.expanduser('~/tmsf/price.txt')

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
        last_count = 0
        last_area = 0
        last_price = 0
        last_total = 0
        last_len = 0

        while True:
            with open(tmsf_file, 'rb') as datafile:
                a_list = pickle.load(datafile)
                length = len(a_list)
                print(a_list)

                if length == last_len:
                    print('unchange data')
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
                        print(pcs_count,pcs_area,pcs_price)

                        last_len = length
                        
            _time.sleep(10)

                

                


                
