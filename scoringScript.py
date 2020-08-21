import json
import joblib
import numpy as np
import pandas as pd
from azureml.core.model import Model

# Called when the service is loaded
def init():
    global model
    # Get the path to the deployed model file and load it
    model_path = Model.get_model_path('devsuccession')
    model = joblib.load(model_path)

# Called when a request is received
def run(Data):
    user_similarity = model[0]
    emplist = pd.DataFrame(model[1], columns =['EmployeeCode', 'Emp_id'])
    EmpCode = json.loads(Data)['EmpCode']
    selectionList = json.loads(Data)['selectionList']
    Emp_id=emplist.loc[emplist['EmployeeCode'] == EmpCode, 'Emp_id'].iloc[0]
    selectionId = list()
    for selectedEmp in range(0,len(selectionList)):
        #print(selectionList[selectedEmp])
        temp=emplist.loc[emplist['EmployeeCode'] == selectionList[selectedEmp], 'Emp_id'].iloc[0]
        selectionId.append(temp)
    selectionId= np.array(selectionId)
    succ_list=np.argsort(user_similarity[Emp_id-1])
    succ_list=np.delete(succ_list, np.where(succ_list == Emp_id-1 ))
    succ_list = succ_list+1
    succ_list=succ_list[np.isin(succ_list,selectionId)]
    succlist = []
    if len(succ_list)>11:
        start=0
        end=10
    else: 
        start=0
        end=len(succ_list)
    for index in range(start,end):
        i=succ_list[index]
        e=int(emplist.loc[emplist['Emp_id'] == i, 'EmployeeCode'].iloc[0])
        print("Index {i} and ECode {e}".format(i=i, e=e))
        succlist.append(e)
    #successors = json.dumps(succlist)
    #print(successors)s
    return succlist
    
