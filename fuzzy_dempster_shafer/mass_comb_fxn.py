# masses are so far a set of 3 for each of the different combination of 0,1. In a dataset, the different masses will be represented
#  by the different columns of the dataset
#  - The entries for the masses are [mass_0,mass_1,mass_01,mass_theta]
# prior0: the prior belief for class 0. Default is uninformative
# prior1: the prior belief for class 1. Default is uninformative
# prior01: the prior belief for both classes. Default is 0

# C0, C1, C01, C_theta are the modified DS beliefs where there is a prior. If no prior is specified, a uniform prior is assumed of equal
#  assignment


def safe_divide(numerator, denominator):
    if (denominator < 0) | (denominator == 0):
        return numerator
    else:
        return (numerator / denominator)


# default prior values are uniform uninformative
def massComb(masses, prior0=0.5, prior1=0.5, prior01=0):

    # the space in the hypothesis space that is not in the evidence space
    prior_theta = 1 - (prior0 + prior1 + prior01)

    # since sum of m(A) must equal 1 there may be frame of descernment is
    # what's left over
    for i in range(len(masses)):
        masses[i].append(1 - sum(masses[i]))

    ##########################
    # PERFORM MASS COMBINATION
    #########################
    print("The different mass functions are:")
    for row in masses:
        print(row)
    intrsxn_array_dim = len(masses[1])
    # set the dimenensions of the mass comb. matrix.
    intrsxn_array = [
        [0 for j in range(intrsxn_array_dim)] for i in range(intrsxn_array_dim)]

    ############### BEGIN: Combining all bpa's ##############################
    for i in range(0,len(masses)-1):
        if i == 0:
            print("first entry")
            K = 1  
            m0 = masses[0][0]
            m1 = masses[0][1]
            m01 = masses[0][2]
            m_theta = masses[0][3]
            print("First mass assignment. m0:", m0, "m1: ", m1,
                  "m01: ", m01, "m_theta: ", m_theta, "K: ", K)

        new_mass = [[m0, m1, m01, m_theta]]
        for col in range(intrsxn_array_dim):
            for row in range(intrsxn_array_dim):
                intrsxn_array[row][col] = new_mass[0][col]*masses[i + 1][row]

        # CALCULATE K - the measure of conflict
        K = intrsxn_array[0][1] + intrsxn_array[1][0]
        # Calculate belief functions
        m0 = (intrsxn_array[0][0] + intrsxn_array[2][0] + intrsxn_array[3][0]
            + intrsxn_array[0][2] + intrsxn_array[0][3]) / (1 - K)
        m1 = (intrsxn_array[1][1] + intrsxn_array[1][2] + intrsxn_array[1][3]
            + intrsxn_array[2][1] + intrsxn_array[3][1]) / (1 - K)
        m01 = intrsxn_array[2][3] / (1 - K)
        # normalize to emphasise agreement
        m_theta = intrsxn_array[3][3] / (1 - K)
        print("Next mass assignment. m0:", m0, "m1: ", m1,
              "m01: ", m01, "m_theta: ", m_theta, "K: ", K)
    ############### END: Combining all bpa's ###############################

    print("m0:", m0, "m1: ", m1, "m01: ",
          m01, "m_theta: ", m_theta, "K: ", K)
    # INCLUDE PRIOR INFORMATION
    print("\n")
    print("prior0: ", prior0, "prior1: ", prior1,
          "prior01: ", prior01, "prior_theta: ", prior_theta)
    # basic certainty assignment (bca) and normalize
    certainty_denominator = (safe_divide(numerator = m0, denominator = prior0) + safe_divide(numerator = m1, denominator = prior1)
                             + 
                             safe_divide(
                                 numerator=m01, denominator=prior01)
                             + safe_divide(numerator=m_theta, denominator=prior_theta))
    print("certainty_denom: ", certainty_denominator)
    C0 = safe_divide(numerator=m0, denominator=prior0) / \
        certainty_denominator
    C1 = safe_divide(numerator=m1, denominator=prior1) / \
        certainty_denominator
    C01 = safe_divide(
        numerator=m01, denominator=prior01) / certainty_denominator
    C_theta = safe_divide(
        numerator=m_theta, denominator=prior_theta) / certainty_denominator
    print("C0: ", C0, "C1: ", C1, "C01: ", C01, "C_theta: ", C_theta)
    print("C0 + C1 + C01 + C_theta: ", C0 + C1 + C01 + C_theta, "\n")

    #print("inrsxn_array:", intrsxn_array[0][1])
    # Belief values: (not used yet, will be important later for multi-class
    # s)
    blf0 = m0
    blf1 = m1
    blf01 = m0 + m1 + m01

    # Plausible values:  (not used yet, will be important)
    plsb0 = m0 + m01 + m_theta
    plsb1 = m1 + m01 + m_theta
    plsb_theta = 1

    mass_fxn_values = {"blf0": blf0, "blf1": blf1, "blf01": blf01, \
                        "plsb0": plsb0, "plsb1": plsb1, "plsb_theta": plsb_theta}

    return (mass_fxn_values)
    # Range of Uncertainty
    #print("Range of uncertainty for case 0: ", "(", blf0, ",", plsb0, ")")
    #print("Range of uncertainty for case 1: ", "(", blf1, ",", plsb1, ")")

    #print("belief0:", blf0, "belief1", blf1, "belief01:", blf01)
    #print("plausible0:", plsb0, "plausible1:", plsb1)
        # calculate K
    # K = (1 - m1)*(m2) + m1*(1 - m2) # K is a measure of conflict

        # joint_mass1 = (1 - m1) * (1 - m2) / (1- K)
        # joint_mass2 = (m1)*(m2) / (1 - K)
        # print (m1, m2,K, joint_mass1, joint_mass2)