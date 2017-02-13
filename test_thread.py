import time, threading, datetime
from multiprocessing import queue

st = datetime.datetime.now()  
while que.qsize() > 0:  
        job = que.get()  
        job.do()  
  
td = datetime.datetime.now() - st  
print("\t[Info] Spending time={0}!".format(td))  