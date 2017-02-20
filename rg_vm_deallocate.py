#!/usr/bin/python
import os
import json
import time
import Queue
import threading
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient

# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret
# AZURE_SUBSCRIPTION_ID: with your Azure Subscription Id
#
# Create the Resource Manager Client with an Application (service principal) token provider
#
subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID') # your Azure Subscription Id
credentials = ServicePrincipalCredentials(
    client_id=os.environ['AZURE_CLIENT_ID'],
    secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant=os.environ['AZURE_TENANT_ID']
    )

client = ResourceManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)
rg_share_name = 'epas-rg-shared'
reserved_rg = 'epas-rg-devqa2-1'

class consumer(threading.Thread):  
    def __init__(self,que):  
        threading.Thread.__init__(self)  
        self.daemon = False  
        self.queue = que  
    def run(self):  
        while True:  
            if self.queue.empty():  
                break  
            rg_name = self.queue.get()
            for vm in compute_client.virtual_machines.list(rg_name):
                st = int(time.time())
                async_vm_deallocate = compute_client.virtual_machines.deallocate( rg_name , vm.name)
                async_vm_deallocate.wait()
                et = int(time.time()) - st # deallocate execution time
                print("Deallocate VM %s in RG %s spend %d seconds\t" % (format(vm.name), rg_name, et))
            self.queue.task_done()  
        return  

def run_queue():
    que = Queue.Queue()

    for rg_list in client.resource_groups.list():
        if rg_list.name not in [rg_share_name, reserved_rg]:
            que.put(format(rg_list.name))

    consumers = [consumer(que) for i in range(0,que.qsize())]

    for c in consumers:
        c.start()
    que.join()
    return

if __name__ == "__main__":
    run_queue()