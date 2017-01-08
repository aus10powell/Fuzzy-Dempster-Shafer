# This function is meant to test the functions involved in training and testing a dataset
import pandas as pd

from test_mass_comb_fxn import *
from test_ds_predict import *
from test_ds_fit import *

from sklearn.model_selection import train_test_split


######
# Changed to run package tests
exit( )
######


# Changed value to True for the dataset you would like to run
if False:
    titanic = pd.read_csv('../data/titanic.csv')
    titanic = titanic[['survived','parch','fare','age']]
    titanic = titanic.dropna()
    # write to R in order to have test against that code
    #titanic.to_csv('titanic_python_testset.csv')

    X_train, X_test, y_train, y_test = train_test_split(titanic, titanic['survived'], test_size = 0.2)
    X_train = X_train.drop(['survived'], axis=1)
    X_test = X_test.drop(['survived'], axis=1)

if False:
    colon = pd.read_csv('../data/colon.csv')
    colon = colon[['sex','age','obstruct','perfor','time','node4','surg','extent']]
    colon = colon.dropna()

    X_train, X_test, y_train, y_test = train_test_split(colon, colon['sex'], test_size = 0.2)
    X_train = X_train.drop(['sex'], axis = 1)
    X_test = X_test.drop(['sex'], axis = 1)

# print the shape of the test file
print('X_test shape:',X_test.shape)



import time

t0 = time.time()



#temp_test = pd.DataFrame(X_test)
fit_object = fit(X_train,y_train)
predictions = predict(fit_object,X_test)

t1 = time.time()
print('runtime: ',t1-t0)

#print('LR probabilities:', predictions['LR_Probabilities'])
#print('LR_plus_DS_Probabilities:', predictions['LR_plus_DS_Probabilities'])
prediction_df = pd.DataFrame(predictions['LR_Probabilities'])
prediction_df['LR_plus_DS_Probabilities'] = predictions['LR_plus_DS_Probabilities']
prediction_df['uncertain'] = predictions['uncertain']

prediction_df.columns = ['LR_Probabilities','LR_plus_DS_Probabilities','uncertain']
print(prediction_df)
#prediction_df.to_csv('testset_predictions.csv')