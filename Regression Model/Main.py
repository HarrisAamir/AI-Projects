from datetime import datetime, timedelta
date_format = '%Y-%m-%d'
import preProccesing2
import regression2
import pandas as pd
import matplotlib.pyplot as plt

date_string = '2016-01-01'
start = datetime.strptime(date_string, date_format)
new_time = start
a=1
Mea=[]
testDates=[]

preProccesing2.initalize()
while(a<22):
    denormalizedDF=preProccesing2.deNormalize(new_time.strftime('%Y-%m-%d'))
    preProccesing2.createTimeSlots(denormalizedDF,new_time.strftime('%Y-%m-%d'))
    if a > 15: #testing of data
     regression2.rollingWindow(new_time.strftime('%Y-%m-%d'))
     Mea.append(regression2.test())
     testDates.append(new_time.strftime('%Y-%m-%d'))

    else : #training of data 
     regression2.rollingWindow(new_time.strftime('%Y-%m-%d'))
    
    new_time = new_time + timedelta(days=1)
    a+=1
data = {'Mean-Absoulute-Error':Mea,
        'Date':testDates}
  
print(Mea)
print(testDates)
df = pd.DataFrame(data) # graph of Mean Absoulute Error
df.plot(x='Date', y='Mean-Absoulute-Error', kind='line')
plt.show()
date_input=datetime.strptime(input("Enter the date (YYYY-MM-DD):"),date_format) 
regionID=input("Enter the Region ID: ")
regression2.UserInput(date_input.strftime('%Y-%m-%d'),regionID)
