#!/usr/bin/python
import os
import json
import time
import Queue
import threading
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient


# get the application credential
subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID') # your Azure Subscription Id
credentials = ServicePrincipalCredentials(
    client_id=os.environ['AZURE_CLIENT_ID'],
    secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant=os.environ['AZURE_TENANT_ID']
    )

client = ResourceManagementClient(credentials, subscription_id)
rg_share_name = ''
#rg_share_name = 'epas-rg-shared'

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
            st = int(time.time())
            client.resource_groups.delete(format(item)).wait()
            et = int(time.time()) - st # delete execution time
            print("Delete RG %s spend %d seconds\t" % (format(item), et))
            self.queue.task_done()  
        return  

def run_queue():
    que = Queue.Queue()

    for items in sorted(client.resource_groups.list()):
        if items.name not in rg_share_name:
            que.put(format(items.name))

    consumers = [consumer(que) for i in range(0,que.qsize())]

    for c in consumers:
        c.start()
    que.join()
    return

if __name__ == "__main__":
    run_queue()
