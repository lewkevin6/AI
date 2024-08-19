############################################################
# CISC3140- P3
# Due May 6th 11:59 Pm
#
################################################################


################################################################################################
#Function to compute the prior count of Label(L): Nursery admission recommendation
#Input: trainFile - train_data.dat
#Returns: priorCountsList- the number of counts for the two classes {recommend, not-recom}
#
################################################################################################
def getPriorCount(trainFile):
    priorCountsList= None
    recommend_count = 0
    not_recom_count = 0
    trainFileObj=open(trainFile,'r')
    trainFileLines=trainFileObj.readlines()
    for trainFileLine in trainFileLines:

        if(trainFileLine.strip('\n').split(',')[-1]) == "recommend":
            recommend_count += 1
        elif(trainFileLine.strip('\n').split(',')[-1]) == "not_recom":
            not_recom_count += 1

    trainFileObj.close()
    return {"recommend":recommend_count, "not_recom": not_recom_count}


################################################################################################
# Function to compute the CPT for each feature: P(O|L) P(N|L) P(F|L) P(C|L) P(H|L) P(I|L) P(S|L) P(A|L)
#                                              Parents occupation (O): {usual, pretentious, great_pret}
#                                              Childs Nursery (N): {proper, less_proper, improper, critical, very_crit}
#                                              Family form (F): {complete, completed, incomplete, foster}
#                                              Number of children (C): {1, 2, 3, more}
#                                              Housing (H): {convenient, less_conv, critical}
#                                              Finance (I): {convenient, inconv}
#                                              Social (S): {non-prob, slightly_prob, problematic}
#                                              Health (A): {recommended, priority, not_recom}
# Inputs: trainFile-train_data.dat, 
#         priorCountList - the number of samples for different label values , 
#         feature_name - This is used to identify which feature the CPT is computed for. 
#                        It can take one of the following values:occupation, nursery, family_form, children, housing, finance, social, health  
# Returns: feature_cpt - The CPT for feature given in feature_name
#
################################################################################################
def getFeatureCPT(trainFile,feature_name, priorCountsList):
    feature_cpt = {}
    recom_count = priorCountsList.get("recommend")
    not_recom_count = priorCountsList.get("not_recom")
    idx = None

    if feature_name == "occupation":
        idx = 0
    elif feature_name == "nursery":
        idx = 1
    elif feature_name == "family_form":
        idx = 2
    elif feature_name == "children":
        idx = 3
    elif feature_name == "housing":
        idx = 4
    elif feature_name == "finance":
        idx = 5
    elif feature_name == "social":
        idx = 6
    elif feature_name == "health":
        idx = 7

    trainFileObj=open(trainFile,'r')
    trainFileLines=trainFileObj.readlines()
    for trainFileLine in trainFileLines:
        # The line is to makes sure that the code executes without error
        #Write your code here
        curr_line = trainFileLine.strip('\n').split(',')

        if curr_line[-1] == "recommend":
            if feature_cpt.get(curr_line[idx] + "_R") == None:
                feature_cpt.update({(curr_line[idx] + "_R"): 1})
            else:
                feature_cpt.update({(curr_line[idx] + "_R"): feature_cpt.get((curr_line[idx] + "_R")) +1})

        elif curr_line[-1] == "not_recom":
            if feature_cpt.get(curr_line[idx] + "_NR") == None:
                feature_cpt.update({(curr_line[idx] + "_NR"): 1})
            else:
                feature_cpt.update({(curr_line[idx] + "_NR"): feature_cpt.get((curr_line[idx] + "_NR")) +1})

    trainFileObj.close()


    for key in feature_cpt:
        if "NR" in key:
            feature_cpt.update({key: feature_cpt.get(key) / not_recom_count})
        else:
            feature_cpt.update({key: feature_cpt.get(key) / recom_count})

    #print(feature_cpt) #For testing
    return feature_cpt


################################################################################################
# Function to predict the labels for the samples in the validation file
#   The label is predicted as max( P(L|O,N, F, C, H, I, S, A)) = max(P(O|L) P(N|L) P(F|L) P(C|L) P(H|L) P(I|L) P(S|L) P(A|L) P(L)) 
#                           That is you will treat the label with maximum probability as the prediction from the above formulation
# Inputs: valFile - val_data.dat
#         priorProb - Prior for the label, Nursery admission recommendation
# Returns: predictions - the predicted label for each sample in valFile
#
################################################################################################
def getPredictions(valFile, priorProb, feature1CPT,feature2CPT,feature3CPT,feature4CPT,feature5CPT,feature6CPT,feature7CPT,feature8CPT):
    predictions= []
    # Write code here

    valFileObj=open(valFile,'r')
    valFileLines=valFileObj.readlines()

    prior_rec = priorProb.get("recommend")
    prior_not_recom = priorProb.get("not_recom")

    for valFileLine in valFileLines:
        curr_line=valFileLine.strip('\n').split(',')
        
        O = curr_line[0]
        N = curr_line[1]
        F = curr_line[2]
        C = curr_line[3]
        H = curr_line[4]
        I = curr_line[5]
        S = curr_line[6]
        A = curr_line[7]
        

        # {'recommended_R': 0.501801931670751, 'priority_R': 0.49819806832924896, 'not_recom_NR': 1.0}

        if(A == "not_recom"):
            predictions.append("not_recom")
        else:
            prediction1 = (prior_rec * feature1CPT.get(O + "_R") *
                                          feature2CPT.get(N + "_R") *
                                          feature3CPT.get(F + "_R") * 
                                          feature4CPT.get(C + "_R") *
                                          feature5CPT.get(H + "_R") *
                                          feature6CPT.get(I + "_R") *
                                          feature7CPT.get(S + "_R") *
                                          feature8CPT.get(A + "_R"))

            prediction2 = (prior_not_recom * feature1CPT.get(O + "_NR") * 
                                          feature2CPT.get(N + "_NR") *
                                          feature3CPT.get(F + "_NR") * 
                                          feature4CPT.get(C + "_NR") *
                                          feature5CPT.get(H + "_NR") *
                                          feature6CPT.get(I + "_NR") *
                                          feature7CPT.get(S + "_NR"))
            
            if prediction1 > prediction2:
                predictions.append("recommend")
            elif prediction1 < prediction2:
                predictions.append("not_recom")
    
    #print(predictions)
    return predictions


if __name__=="__main__":
    trainFile= "train_data.dat"
    valFile= "val_data.dat"
    priorCountsList=getPriorCount(trainFile)
    #Write code to compute the priorPob from the priorCountsList and assign it to PriorProb
    #You will pass the computed priorProb to getPredictions
    priorProb = {"recommend": priorCountsList.get("recommend") / (priorCountsList.get("recommend") + priorCountsList.get("not_recom")),
                 "not_recom": priorCountsList.get("not_recom") / (priorCountsList.get("recommend") + priorCountsList.get("not_recom"))
                }
    
    print("Prior Count", priorCountsList, "\n")
    print("Prior Probablitlies", priorProb, "\n")

    occupationCPT=getFeatureCPT(trainFile,"occupation", priorCountsList)
    nurseryCPT=getFeatureCPT(trainFile,"nursery",priorCountsList)
    familyFormCPT=getFeatureCPT(trainFile,"family_form",priorCountsList)
    childrenCPT=getFeatureCPT(trainFile,"children",priorCountsList)
    housingCPT=getFeatureCPT(trainFile,"housing",priorCountsList)
    financeCPT=getFeatureCPT(trainFile,"finance",priorCountsList)
    socialCPT=getFeatureCPT(trainFile,"social",priorCountsList)
    healthCPT=getFeatureCPT(trainFile,"health",priorCountsList)

    lineCounter=0
    correctCount=0
    totalCount=0
    predictList=getPredictions(valFile, priorProb, occupationCPT, nurseryCPT, familyFormCPT, childrenCPT, housingCPT, financeCPT, socialCPT, healthCPT)
    valFileObj=open(valFile,'r')
    valFileLines=valFileObj.readlines()

    for valFileLine in valFileLines:
        label=valFileLine.strip('\n').split(',')[-1]
        if label==predictList[lineCounter]:
            correctCount+=1
        totalCount+=1
        lineCounter+=1
    
    valFileObj.close()

    print("The accuracy of the current predictions is {}".format((correctCount/totalCount)*100))
