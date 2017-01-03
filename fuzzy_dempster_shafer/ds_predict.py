##### PREDICTION FUNCTION
## Variables description
# train_object - valid data frame
# y_train - Specify your binary response variable

# measure_belief - (default value set to 1) the measure of belief
# uncertainty - (default value set to 0.1) the measure of uncertainty
# uncertainty_ab - (default value set to 0.055 the measure of uncertainty for overlapping classes
# last - a logical for whether the current fit is the final fit. Used primarily because of caret package
# lev -  the class levels of the outcome (or NULL in regression). For future model modification into more than binary outcome.
# classProbs - a logical for whether class probabilities should be computed.
# other setting the minimum value for set overlap
# belief_increase
# belief_decrease

## Dependencies
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np

def predict(train_object, X_test,
                 measure_belief = 0.89, uncertainty = 0.1, 
                 uncertainty_ab = 0.055, other = 0.01,
                 belief_increase = 0.2, belief_decrease = 0.2):
    
    #X_test = pd.DataFrame(X_test) # don't think this is necessary
    
    
    clf = train_object[1]
    probabilities = clf.predict_proba(X_test)  
    probabilities = pd.DataFrame(probabilities).ix[:,1] # probabilities of classifying as '1'
    classifications = clf.predict(X_test)
    
    train_object = train_object[0]
    X_test = pd.DataFrame(X_test)
    
    # Initializing dataframes for the mass functions
    mass_min0 = mass_min1 = mass_0and1 = mass_0 = mass_1 \
    = pd.DataFrame(np.nan,index=range(X_test.shape[0]), columns=range(X_test.shape[1]))
    
    
    # iterate through columns of test data set
    for j in range(X_test.shape[1]):
        
        # iterate through columns of test data set
        for i in range(X_test.shape[0]):
            obs = X_test.iloc[i][j]  # variable used to make code more read-able
            
            # Condition 1
            if obs <= train_object.ix[j,'max0'] and obs < train_object.ix[j,'min1']:
                mass_min0[j][i] = measure_belief
                mass_min1[j][i] = other
                mass_0and1[j][i] = uncertainty
            # Condition 2
            elif (obs > train_object.ix[j,'max0'] and obs < train_object.ix[j,'min1']) or \
                     (obs <= train_object.ix[j,'max0'] and obs >= train_object.ix[j,'min1']  \
                      and obs <= train_object.ix[j,'max1'] \
                      and train_object.ix[j,'max0'] < train_object.ix[j,'max1']):
                mass_min0[j][i] = uncertainty_ab
                mass_min1[j][i] = uncertainty_ab
                mass_0and1[j][i] = uncertainty                    
            # Condition 3    
            elif (obs <= train_object.ix[j,'max0'] and obs >= train_object.ix[j,'min1'] \
                 and obs <= train_object.ix[j,'max1'] and train_object.ix[j,'max0'] >= train_object.ix[j,'max1']):
                mass_min0[j][i] = uncertainty
                mass_min1[j][i] = other
                mass_0and1[j][i] = measure_belief
            # Condition 4
            elif (obs <= train_object.ix[j,'max0'] and obs > train_object.ix[j,'max1']) or \
                 (obs > train_object.ix[j,'max0'] and obs > train_object.ix[j,'max1'] \
                 and train_object.ix[j,'max0'] >= train_object.ix[j,'max1']):
                mass_min0[j][i] = measure_belief
                mass_min1[j][i] = other
                mass_0and1[j][i] = uncertainty  
            # Condition 5
            elif (obs > train_object.ix[j,'max0'] and obs <= train_object.ix[j,'max1'] and obs >= train_object.ix[j,'min1']) \
                or (obs > train_object.ix[j,'max0'] and obs > train_object.ix[j,'max1'] \
                    and train_object.ix[j,'max1'] > train_object.ix[j,'max0']):
                mass_min0[j][i] = other
                mass_min1[j][i] = measure_belief
                mass_0and1[j][i] = uncertainty 
            else:
                print("Something has gone wrong with your script or max/min values")
            
            # Checking which mass values matrix is "benign" and which is "malignant"
            if train_object.ix[j,'lower_class'] == 0:
                #mass_0.iloc[i][j] = mass_min0.iloc[i][j] # probably exactly the same
                #mass_1.iloc[i][j] = mass_min1.iloc[i][j] # probably exactly the same
                mass_0[j] = mass_min0[j] # old code, probably works though didn't make sure
                mass_1[j] = mass_min1[j] # old code, probably works though didn't make sure
            else: 
                #mass_0.iloc[i][j] = mass_min1.iloc[i][j]# probably exactly the same
                #mass_1.iloc[i][j] = mass_min0.iloc[i][j]# probably exactly the same
                mass_1[j] = mass_min0[j] 
                mass_0[j] = mass_min1[j]
    
    # Create belief/unbelief/uncertainty values
    ## R-code
    # for(j in 1:ncol(newdata)){
    #masses[[j]] <- mass(list("0"=mass_0[i,j], "1"=mass_1[i,j], "0/1"=mass_0and1[i,j]), stateSpace) 
    #}
    # mass_combo = mComb(masses, list("0" = 1-probabilities[i], "1" = probabilities[i]))
    
    for i in range(X_test.shape[0]):
        masses = []
        for j in range(X_test.shape[1]):
            masses.append([mass_0.iloc[i][j],mass_1.iloc[i][j],mass_0and1.iloc[i][j]])
    ## commenting out until I can figure why masses aren't working
    mass_combo = massComb(masses,prior0 = (1 - probabilities), prior1 = probabilities, prior01 = 0)
    # mass_combo = massComb(masses, prior0 = (1 - probabilities), prior1 = probabilities, prior01=0) 

    return(mass_combo)



