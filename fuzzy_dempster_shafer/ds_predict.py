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

# temporary files for testing
#from test_mass_comb_fxn import *
# temporary files for testing

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
                #mass_0.iloc[i][j] = mass_min0.iloc[i][j] 
                #mass_1.iloc[i][j] = mass_min1.iloc[i][j] 
                mass_0[j] = mass_min0[j] 
                mass_1[j] = mass_min1[j] 
            else: 
                #mass_0.iloc[i][j] = mass_min1.iloc[i][j]
                #mass_1.iloc[i][j] = mass_min0.iloc[i][j]
                mass_1[j] = mass_min0[j] 
                mass_0[j] = mass_min1[j]
    

    # Initialize vectors for holding the classifications made by D-S theory
    ## belief and belief0 are beliefs in 1 and 0 respectively
    LR_plus_DS_probs = LR_plus_DS_classi  = \
    belief = belief0 = \
    lower_bound_1 = lower_bound_0 = upper_bound_1 = upper_bound_0 = \
    uncertain = disbelief = \
    np.zeros(X_test.shape[0])

    
    for i in range(X_test.shape[0]):
        masses = []
        for j in range(X_test.shape[1]):
            masses.append([mass_0.iloc[i][j], mass_1.iloc[i][j], mass_0and1.iloc[i][j]])

        mass_combo = massComb(masses, prior0 = (1 - probabilities[i]), prior1 = probabilities[i], prior01 = 0)

        belief[i] = mass_combo['blf1'] # belief is a degree of evidence
        belief0[i] = mass_combo['blf0']
        uncertain[i] = mass_combo['plsb1'] - mass_combo['blf1'] # uncertainty is the difference between plausability of a value of 1 and belief of a value of 1
        disbelief[i] = 1 - (mass_combo['blf1'] + mass_combo['blf01']) # Disbelief is the compliment to plausability (something we don't condsider possbile)

        # Calculating uncertain "confidence intervals". From most literature this should also include plausability of parameter space
        # However, it does not appear that the mass_comb fxn currently supports probabilities that don't add to 1
        lower_bound_1[i] = belief[i]
        upper_bound_1[i] = belief[i] + uncertain[i]
        lower_bound_0[i] = belief0[i]
        upper_bound_0[i] = belief0[i] + uncertain[i]


    for i in range(X_test.shape[0]):
        if (belief[i] > 0.5) and (classifications[i] == 1):
            LR_plus_DS_probs[i] = probabilities[i] + belief_increase        
            if LR_plus_DS_probs[i] > 1:
                LR_plus_DS_probs[i] = 1
        elif (belief[i] > 0.5) and (classifications[i] == 0):
            LR_plus_DS_probs[i] = probabilities[i] + belief_increase
            if LR_plus_DS_probs[i] > 1:
                LR_plus_DS_probs[i] = 1
        elif (disbelief[i] > 0.5) and (classifications[i] == 1):
            LR_plus_DS_probs[i] = probabilities[i] - belief_decrease
            if LR_plus_DS_probs[i] < 0:
                LR_plus_DS_probs[i] = 0
        elif (disbelief[i] > 0.5) and (classifications[i] == 0):
            LR_plus_DS_probs[i] = probabilities[i] - belief_decrease
            if LR_plus_DS_probs[i] < 0:
                LR_plus_DS_probs[i] = 0
        else:
            LR_plus_DS_probs[i] = probabilities[i]

        if LR_plus_DS_probs[i] > 0.5:
            LR_plus_DS_classi[i] = 1
        else:
            LR_plus_DS_classi[i] = 0

    output_to_return = {"LR_Classifications": classifications, "LR_Probabilities": probabilities, "LR_plus_DS_Classifications": LR_plus_DS_classi, \
                         "LR_plus_DS_Probabilities": LR_plus_DS_probs, "lower_bound_1": lower_bound_1, "upper_bound_1": upper_bound_1, \
                         "lower_bound_0": lower_bound_0, "upper_bound_0": upper_bound_0, "uncertain": uncertain}

    return (output_to_return)


