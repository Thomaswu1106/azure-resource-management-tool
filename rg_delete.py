import os
import json
import time
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

    # List Resource Groups

    print('List RGs : ')
    for item in client.resource_groups.list():
        print('Start to delete RG : ' + format(item.name) + '\t')
        #delete_async_operation = client.resource_groups.delete(format(item.name))
        st = int(time.time())
        client.resource_groups.delete(format(item.name))
        print(int(time.time()) - st)

    def delete():
    """ Resource delete function """
        print("Test threading at time %s", time.ctime(time.time()))
        return


if __name__ == "__main__":
    run_example()