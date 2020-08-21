import json


# Convert the array to a serializable list in a JSON document
input_json = sample_input = json.dumps({
    'EmpCode': 17098,
    'selectionList':[17099
,17125
,17127
,17173
,17186
,17188
,17201
,17304
,17330
,17338
,17348
,17349
]
})

endpoint = "http://a7b13c94-3a5f-4a67-8efc-1262bec99d4f.southeastasia.azurecontainer.io/score"
headers = { 'Content-Type':'application/json' }

predictions = requests.post(endpoint, input_json , headers = headers)
predicted_classes = predictions.json()
requests.


response = requests.post(,
                         headers=aad_token,
                         json={"ExperimentName": "My_Pipeline",
                               "ParameterAssignments": {"pipeline_arg": 20}})

from azureml.core.authentication import ServicePrincipalAuthentication

sp = ServicePrincipalAuthentication(tenant_id="e95e330a-6410-4dd1-a705-575cba48e853", # tenantID
                                    service_principal_id="306d65da-1788-4088-939e-b1c40bea9c0c", # clientId
                                    service_principal_password="RzHm3X-Xv_Ubc~q-R89rdLZHQGK_VH.1v7")

from adal import AuthenticationContext

client_id = "306d65da-1788-4088-939e-b1c40bea9c0c"
client_secret = "RzHm3X-Xv_Ubc~q-R89rdLZHQGK_VH.1v7"
resource_url = "https://login.microsoftonline.com"
tenant_id = "e95e330a-6410-4dd1-a705-575cba48e853"
authority = "{}/{}".format(resource_url, tenant_id)

auth_context = AuthenticationContext(authority)
token_response = auth_context.acquire_token_with_client_credentials("https://management.azure.com/", client_id, client_secret)
print(token_response)