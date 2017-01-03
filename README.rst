Fuzzy Dempster:
---------------

### Synopsis
This is an ongoing project to creating a machine learning classification package. The highlight of this package will be the utilization of Dempster-Shafer theory to improve on classifications from other methods such as logistic regression.

### Code Example
* Train the model: assign subjective probabilites (masses) to all subsets of the data.
* Predict the the data

### Motivation
Dempster-Shafer theory in general attempts to consolidate evidence. It starts withe possibilities under consideration and partitions them into belief (strength of evidence) and plausibility (the set of all possible values including the evidence. 

In practice, the algorithm is believed to improve (even if only marginally) the performance of classifications through other probabilities such as logistic regression. It can effectively be used on many different types of data, particularly images where evidence could theoretically be gathered to classify what the image is representing. 

### Installation
In progress

### Current Effort
Optimize parameters for belief increase or decrease using grid search. Later to be an optimized grid search.
