import azureml.core
from azureml.core import Workspace, Experiment
import joblib
from scipy import spatial
import pandas as pd 
import numpy as np
import argparse
from azureml.core.authentication import ServicePrincipalAuthentication
#test2
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
# Load the workspace from the saved config file
#ws = Workspace.from_config()
print('Ready to use Azure MLL {} to work with {}'.format(azureml.core.VERSION, ws.name))
experiment = Experiment(workspace = ws, name = "successionPlanning")
run = experiment.start_logging(snapshot_directory=None)
print("Starting experiment:", experiment.name)


parser = argparse.ArgumentParser()
parser.add_argument('-data','--data', type=str, dest='data', help='data')
args = parser.parse_args()
data = args.data
print(data)
df=pd.read_json(data)

emplist=pd.DataFrame({'EmployeeCode':df.EmployeeCode.unique()})
emplist['Emp_id']=(np.arange(len(emplist)))+1
namelist = pd.DataFrame({'Name':df.Name.unique()})
namelist['Name_id']=(np.arange(len(namelist)))+1
df=df.join(emplist.set_index('EmployeeCode'), on='EmployeeCode')
df=df.join(namelist.set_index('Name'), on='Name')

#creating the matrix
n_users = df.EmployeeCode.unique().shape[0]
n_items = df.Name.unique().shape[0]

data_matrix = np.zeros((n_users, n_items))
for line in df.itertuples():
    data_matrix[line[4]-1, line[5]-1] = line[3]
    

def adjusted_cos_distance_matrix(size, matrix, row_column):
    distances = np.zeros((size,size))
    if row_column == 0:
        M_u = matrix.mean(axis=1)
        m_sub = matrix - M_u[:,None]
    if row_column == 1:
        M_u = matrix.T.mean(axis=1)
        m_sub = matrix.T - M_u[:,None]
    for first in range(0,size):
        for sec in range(0,size):
            distance = spatial.distance.cosine(m_sub[first],m_sub[sec])
            distances[first,sec] = distance
    return distances
user_similarity = adjusted_cos_distance_matrix(n_users,data_matrix,0)
item_similarity = adjusted_cos_distance_matrix(n_items,data_matrix,1)
listEmployee=emplist.values.tolist()
modelList = [user_similarity,listEmployee]
#Save the trained model
model_file = 'devsuccession.pkl'
joblib.dump(value= modelList , filename=model_file)
run.upload_file(name = model_file, path_or_stream = './' + model_file)

# Complete the run
run.complete()

# Register the model
run.register_model(model_path='./devsuccession.pkl', model_name='devsuccession',
                    tags={'Training context':'Inline Training'})
# print(data2)
print('Model trained and registered.')