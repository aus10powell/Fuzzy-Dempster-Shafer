##### TRAINING FUNCTION

## Dependendicies
import pandas as pd  
import numpy as np
from sklearn.linear_model import LogisticRegression

def fit(X_train,y_train, measure_belief=0.89, uncertainty=0.1,
             uncertainty_ab=0.055, other = 0.01, belief_inc = 0.2, belief_dec = 0.2):

    X_train = pd.DataFrame(X_train)

    
    # Scaling/normalizing the data
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler() 
    df_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns) 
    
    clf = LogisticRegression()
    fitted_model = clf.fit(df_scaled.as_matrix(), y_train.as_matrix())
    y_train = pd.DataFrame(y_train) 
    
    #Partitioning the training dataset by class
    class_index = y_train.loc[y_train.ix[:, 0] == 0].index
    train_class_0 = pd.DataFrame(df_scaled, index = class_index)
    class_index = y_train.loc[y_train.ix[:, 0] == 1].index  
    train_class_1 = pd.DataFrame(df_scaled, index = class_index)
    

    # Loops to train model on the data and pass to prediction function 
    # use it to classify the testing examples
    # Getting the mins and maxs from each partition of the dataset
    # lower_class is the one with the lower min value, making note if lower_class is class 0 or 1  
    df_mins_max = pd.DataFrame(np.nan,index=range(len(train_class_0.columns)), 
        columns=['min0','max0', 'min1','max1','lower_class'])

    for i in range(len(train_class_0.columns)):
        if pd.DataFrame.min(train_class_0)[i] > pd.DataFrame.min(train_class_1)[i]:   
           df_mins_max.loc[i, 'min0'] = pd.DataFrame.min(train_class_1)[i]
           df_mins_max.loc[i, 'max0'] = pd.DataFrame.max(train_class_1)[i]
           df_mins_max.loc[i, 'min1'] = pd.DataFrame.min(train_class_0)[i]
           df_mins_max.loc[i, 'max1'] = pd.DataFrame.max(train_class_0)[i]
           df_mins_max.loc[i, 'lower_class'] = 1
        else:    
           df_mins_max.loc[i, 'min0'] = pd.DataFrame.min(train_class_0)[i]
           df_mins_max.loc[i, 'max0'] = pd.DataFrame.max(train_class_0)[i]
           df_mins_max.loc[i, 'min1'] = pd.DataFrame.min(train_class_1)[i]
           df_mins_max.loc[i, 'max1'] = pd.DataFrame.max(train_class_1)[i]
           df_mins_max.loc[i, 'lower_class'] = 0

    return df_mins_max, fitted_model


	    

