import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from numpy import arange
import numpy as np
from sklearn.metrics import mean_absolute_error
model = LinearRegression()
testXarr=[]
testYarr=[]
Date=''
#fucntion to train data on rolling window
def rollingWindow(date):
    print("Training for "+date)
    regionId=0
    global Date
    Date=date
    while(regionId<66):
        timeCount= pd.read_csv("TimeCounts/"+date+"/count-table-R"+str(regionId+1)+".csv")
        windowSize=10
        starting=0
        ending=starting+windowSize
        Xarr=[]
        Yarr=[]
        while ending<142:
            ending=starting+windowSize
            newDf= timeCount.iloc[starting:ending]
            newDf = newDf.drop('TimeSlot',axis= 1).drop('weather',axis= 1).drop('temperature',axis= 1).drop('PM2.5',axis= 1).drop('i',axis= 1)
            X = newDf['Gapij'].tolist()
            #X= X.to_numpy().reshape(-1, 1)
            Xarr.append(X)
            testXarr.append(X)
            y = timeCount['Gapij'].iat[ending+1]
            Yarr.append(y)
            testYarr.append(y)
            starting+=1
        
        regionId+=1
        global model
        model.fit(Xarr,Yarr)

#Fucntion to test the model
def test():
    print("Testing for date "+Date)
    predictedResults=[]
    for x in testXarr:
        inputarr=[]
        inputarr.append(x)
        modelPrediction=model.predict(inputarr)
        predictedResults.append(modelPrediction[0])
    print("----------------")
    mae = mean_absolute_error(testYarr, predictedResults)
    print("MEA for "+Date+" :"+str(mae))
    print("----------------")
    return mae

#fucntion to predict value on user inputs
def UserInput(date,region):
    regionId=region
    timeCount= pd.read_csv("TimeCounts/"+date+"/count-table-R"+str(regionId)+".csv")
    windowSize=10
    starting=0
    ending=starting+windowSize
    Xarr=[]
    Yarr=[]
    while ending<142:
            ending=starting+windowSize
            newDf= timeCount.iloc[starting:ending]
            newDf = newDf.drop('TimeSlot',axis= 1).drop('weather',axis= 1).drop('temperature',axis= 1).drop('PM2.5',axis= 1).drop('i',axis= 1)
            X = newDf['Gapij'].tolist()
            #X= X.to_numpy().reshape(-1, 1)
            Xarr.append(X)
            testXarr.append(X)
            y = timeCount['Gapij'].iat[ending+1]
            Yarr.append(y)
            testYarr.append(y)
            starting+=1
        
    inputs=[]
    global model
    model.fit(Xarr,Yarr)
    for i in range(10):
       inputs.append(int(input("Enter the Gap of TimeSlot: "+str(i+1))))
    inputArr=[]
    inputArr.append(inputs)
    print("Predicted Result: "+str(model.predict(inputArr)[0]))
    

  