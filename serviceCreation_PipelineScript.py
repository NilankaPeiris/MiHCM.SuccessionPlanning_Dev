from azureml.core.model import InferenceConfig
from azureml.core import Model
from azureml.core import Workspace
from azureml.core.webservice import AciWebservice
from azureml.core.webservice import Webservice
from azureml.core.environment import Environment
from azureml.core.authentication import ServicePrincipalAuthentication

environment = Environment("LocalDeploy")
environment.python.conda_dependencies.add_pip_package("scipy")
environment.python.conda_dependencies.add_pip_package("joblib")
environment.python.conda_dependencies.add_pip_package("numpy")
environment.python.conda_dependencies.add_pip_package("pandas")

inference_config = InferenceConfig(entry_script="./scoringScript.py",
                                   environment=environment)
svc_pr_password = "RzHm3X-Xv_Ubc~q-R89rdLZHQGK_VH.1v7"

svc_pr = ServicePrincipalAuthentication(
    tenant_id="e95e330a-6410-4dd1-a705-575cba48e853",
    service_principal_id="306d65da-1788-4088-939e-b1c40bea9c0c",
    service_principal_password=svc_pr_password)


ws = Workspace(
    subscription_id="5d1ef591-e4ab-4034-9f30-dbc22ff30a17",
    resource_group="rgSuccessionPlanning",
    workspace_name="wsSuccessionPlanning",
    auth=svc_pr
    )
model = ws.models['devsuccession']

deployment_config = AciWebservice.deploy_configuration(cpu_cores = 1, memory_gb = 1)

service_name = "successionplanning-service"

try:
    service = Webservice(name=service_name, workspace=ws)
    service.update(models=[model], inference_config=inference_config)
    print(service.state)
except:
    service = Model.deploy(ws, service_name, [model], inference_config, deployment_config)

    service.wait_for_deployment(True)
    print(service.state)