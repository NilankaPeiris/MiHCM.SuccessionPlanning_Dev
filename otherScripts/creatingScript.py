from azureml.core import Workspace
from azureml.core.compute import ComputeTarget
#from azureml.core.compute import AmlCompute
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
import json
from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import Pipeline
from azureml.core import Experiment
cluster_name = "SuccPlanning-nilanka"
ws = Workspace.from_config()

#creating the cluster 
pipeline_cluster = ComputeTarget(workspace=ws, name="SuccPlanning-nilanka")


# Create a Python environment for the experiment
environment = Environment("diabetes-pipeline-env")

# Use a docker container

environment.python.conda_dependencies.add_pip_package("scipy")
environment.python.conda_dependencies.add_pip_package("joblib")
environment.python.conda_dependencies.add_pip_package("numpy")
environment.python.conda_dependencies.add_pip_package("pandas")


# Create a new runconfig object for the pipeline
pipeline_run_config = RunConfiguration()

# Use the compute you created above. 
pipeline_run_config.target = pipeline_cluster

# Assign the environment to the run configuration
pipeline_run_config.environment = environment

print ("Run configuration created.")
pipeline_param = PipelineParameter(
  name="data",
  default_value=default)
register_step = PythonScriptStep(name = "Register Model",
                                script_name = "pipelineScript.py",
                                arguments = ['--data', pipeline_param],
                                compute_target = pipeline_cluster,
                                runconfig = pipeline_run_config,
                                allow_reuse = True)
reg_pipeline=Pipeline(workspace=ws,steps=[register_step])


# Submit the pipeline to be run
pipeline_run1 = Experiment(ws, 'RegExp3').submit(reg_pipeline)
pipeline_run1.wait_for_completion()