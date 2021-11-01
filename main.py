import os
import time
import threading
import datetime

class Counter:
    def __init__(self, min=10):
        self.sec = min*60
    def start(self):
        self.t0 = time.time()
    def is_timeout(self):
        now = time.time()
        if now - self.t0 > self.sec:
            return True
        else:
            return False
        

def show_dialog():
    global res
    res = 'init'
    res = os.popen("""osascript -e 'tell app "System Events" to display dialog "Close your eyes for 20 sec\n\n%s\nCancel to postpone for 3 mins\n"'"""%(str(datetime.datetime.now()))).read()


def say_count_down(break_min=20/60):
    global res
    assert break_min >= 11/60
    tcounter = Counter(min=break_min-10/60)
    tcounter.start()
    while True:
        time.sleep(1)
        if tcounter.is_timeout():
            break
        if res != 'init':
            break
    if res == 'init':
        for i in range(10):
            i = 10 - i
            if i in [10, 5, 3, 2, 1]:
                os.system("say %d"%i)
            time.sleep(1)
            if res != 'init':
                break
        if res == 'init':
            os.system("say continue your work")



def close_eyes(working_min=10, break_min=20/60, postpone_min=3):
    global res
    is_postpone = False
    is_first_time = True
    while True:
        print('')
        if is_postpone:
            sec = postpone_min * 60
        else:
            sec = working_min * 60
        # if not is_first_time:
        if True:
            # print('counting... %s mins'%working_min)
            time.sleep(sec)
        else:
            print('pass sleep for first time')
        do_show_dialog = threading.Thread(target=show_dialog)
        threading.Thread(target=lambda:os.system("say close your eye now now now")).start()

        break_counter = Counter(min=break_min)
        do_say_count_down = threading.Thread(target=say_count_down, args=(break_min,))
        do_show_dialog.start()
        do_say_count_down.start()
        break_counter.start()
        while True:
            if res != 'init':
                break
            if break_counter.is_timeout():
                break
        
        # wait until has input
        do_show_dialog.join()
        do_say_count_down.join()
        if 'ok' in res.lower():
            is_postpone = False
            ans = 'rest'
        else:
            is_postpone = True
            ans = 'postpone'

        print(datetime.datetime.now(), ans)
        with open('log.txt', 'a') as f:
            f.write(str(datetime.datetime.now())+' '+str(ans))
        
        is_first_time = False

# global
res = 'init'
mode = ''

if __name__ == '__main__':
    def get_time_str(min):
        is_min = True if min >=1 else False
        if is_min:
            return  '%d minutes'%min
        else:
            sec = min * 60
            return '%d seconds'%sec

    working_min = 10
    break_min = 20/60
    postpone_min = 3
    w = get_time_str(working_min)
    b = get_time_str(break_min)
    p = get_time_str(postpone_min)
    print('''
---##############---
 working\t%s
 break\t\t%s
 postpone\t%s
####################
    '''%(w,b,p))
    close_eyes(working_min=working_min, break_min=break_min, postpone_min =postpone_min)
