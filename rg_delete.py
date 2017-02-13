import os
import json
import time
import Queue
import threading
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient

# Manage resources and resource groups - create, update and delete a resource group,
# deploy a solution into a resource group, export an ARM template. Create, read, update
# and delete a resource
#
# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret
# AZURE_SUBSCRIPTION_ID: with your Azure Subscription Id
#

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
            print('Start to delete RG : ' + format(item.name) + '\t')
            st = int(time.time())
            client.resource_groups.delete(format(item.name)).wait()
            print(int(time.time()) - st)
            #processing the item
            #time.sleep(item)
            #print self.name,item  
            self.queue.task_done()  
        return  

def run_example():
    """Resource Group management example."""
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

    que = Queue.Queue()
    for items in client.resource_groups.list():
        que.put(items.name)

    consumers = [consumer(que) for i in que.qsize()]

    for a in consumers:
        c.start()
    que.join()

'''
    # List Resource Groups
    print('List RGs : ')
    for item in client.resource_groups.list():
        print('Start to delete RG : ' + format(item.name) + '\t')
        st = int(time.time())
        client.resource_groups.delete(format(item.name)).wait()
        print(int(time.time()) - st)
'''

if __name__ == "__main__":
    run_example()