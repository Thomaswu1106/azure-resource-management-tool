import time
import random
import Queue
import threading

class consumer(threading.Thread):  
    def __init__(self,que):  
        threading.Thread.__init__(self)  
        self.daemon = False  
        self.queue = que  
    def run(self):  
        while True:  
            if self.queue.empty():  
                break  
            item = self.queue.get()  
            #processing the item  
            time.sleep(item)  
            print ('Thread name %s sleep %.5f second' % (self.name, item))
            self.queue.task_done()  
        return  
que = Queue.Queue()  
for x in range(10):  
    que.put(random.random() * 10, True, None)  
consumers = [consumer(que) for i in range(10)]

print 'Queue numbers is %s' % que.qsize()

for c in consumers:  
    c.start()  
que.join()  
