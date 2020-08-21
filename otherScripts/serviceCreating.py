from azureml.core.model import InferenceConfig
from azureml.core import Model
from azureml.core import Workspace
#from azureml.core.keyvault import Keyvault

from azureml.core.environment import Environment

environment = Environment("LocalDeploy")
environment.python.conda_dependencies.add_pip_package("scipy")
environment.python.conda_dependencies.add_pip_package("joblib")
environment.python.conda_dependencies.add_pip_package("numpy")
environment.python.conda_dependencies.add_pip_package("pandas")

# inference_config = InferenceConfig(runtime= "python",
#                                    source_directory ="C:/Users/NilankaPeiris/Desktop/Microimage/Dev/MiHCM.Analytics.SuccessionPlanning/test" ,
#                                    entry_script="C:/Users/NilankaPeiris/Desktop/Microimage/Dev/MiHCM.Analytics.SuccessionPlanning/test/otherScripts/scoringScript.py",
#                                    conda_file="C:/Users/NilankaPeiris/Desktop/Microimage/Dev/MiHCM.Analytics.SuccessionPlanning/test/successionPlanningEnv.yml")

inference_config = InferenceConfig(entry_script="C:/Users/NilankaPeiris/Desktop/Microimage/Dev/MiHCM.Analytics.SuccessionPlanning/test/otherScripts/scoringScript.py",
                                   environment=environment)
ws = Workspace.from_config()
model = ws.models['devsuccession']

from azureml.core.webservice import LocalWebservice

# This is optional, if not provided Docker will choose a random unused port.
deployment_config = LocalWebservice.deploy_configuration(port=6789)

local_service = Model.deploy(ws, "test", [model], inference_config, deployment_config)


print('Local service port: {}'.format(local_service.port))

print(local_service.get_logs())