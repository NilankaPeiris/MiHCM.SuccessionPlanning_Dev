published_pipeline = succ_pipeline.publish(name="succ_Planning_Reg_Sevice_Model3",
                                      description="Trains model and Creates the Service",
                                      version="1.0")
rest_endpoint = published_pipeline.endpoint
print(rest_endpoint)

from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication()
auth_header = interactive_auth.get_authentication_header()

import requests
experiment_name = 'RegExp3'

response = requests.post(rest_endpoint, 
                         headers=auth_header, 
                         json={"ExperimentName": experiment_name,
                               "ParameterAssignments": {"data": default}})
run_id = response.json()["Id"]
run_id