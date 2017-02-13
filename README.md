---
services: Azure resource delete
platforms: python
author: Thomas
---

# Manage Azure resources and resource groups with Python

This sample explains how to manage your
[resources and resource groups in Azure](https://azure.microsoft.com/en-us/documentation/articles/resource-group-overview/#resource-groups)
using the Azure Python SDK.

**On this page**

- [Run this sample](#run)
- [What is rg_delete.py doing?](#example)


<a id="run"></a>
## Run this sample

1. If you don't already have it, [install Python](https://www.python.org/downloads/).

2. We recommend to use a [virtual environnement](https://docs.python.org/3/tutorial/venv.html) to run this example, but it's not mandatory. You can initialize a virtualenv this way:

    ```
    pip install virtualenv
    virtualenv mytestenv
    cd mytestenv
    source bin/activate
    ```

3. Install the dependencies using pip.

    ```
    cd azure-resource-management-tool
    pip install -r requirements.txt
    ```

4. Create an Azure service principal either through
[Azure CLI](https://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal-cli/),
[PowerShell](https://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/)
or [the portal](https://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/).

6. Export these environment variables into your current shell. 

    ```
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    export AZURE_SUBSCRIPTION_ID={your subscription id}
    ```

7. Run the sample.

    ```
    python rg_delete.py
    ```

<a id="example"></a>
## What is rg_delete.py doing?

The sample walks you through delete all of resource group in specific subscription.
It starts by setting up a ResourceManagementClient object using your subscription and credentials.
