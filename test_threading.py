import os
import json
import time
import threading

def print_time( thread_name, delay ):
    count = 0
    while count < 5:
        time.sleep()
        count += 1
        print ("%s : %s", thread_name, time.ctime(time.time()))

try:
    thread.start_new_thread( print_time, ("Thread-1",2))
    thread.start_new_thread( print_time, ("Thread-2",4))

except:
    print("Error: unable to start thread")