from datetime import datetime, timedelta
date_format = '%Y-%m-%d %H:%M:%S'
import pandas as pd
weatherDF=''
orderDF=''
regionDF=''
poiDF=''

def initalize():
   global poiDF
   poiDF=generatePoiDF()
   global regionDF
   regionDF=generateRegionDF()

#denormalization 
def deNormalize(date):
   print("Denormalization started for "+date)
   orderDF=generateOrderDF(date)
   join= pd.merge(orderDF, regionDF, left_on='start_region_hash', right_on='region_hash',suffixes=('_start','_startHash'))
   join= pd.merge(join, poiDF, left_on='start_region_hash', right_on='region_hash',suffixes=('_des','_desHash')) 
   join=join.drop(columns=['region_hash_des','region_hash_desHash'])
   join=join.sort_values(by=['Time'])
   csvFilename="Denormalized/deNormalized_table_"+date+".csv"
   join.to_csv(csvFilename, index=False)
   print(f'Denormalization complete for {date}, check Denormalized folder')
   return join
#reading weather datas
def generateWeatherDF(date):
    filename="Weather/weather_data_"+date
    f= open(filename,"r")
    filedata=f.read()
    rows=filedata.splitlines()
    time=[]
    weather=[]
    temperature=[]
    pm25=[]
    for row in rows:
        col=row.split("\t")
        time.append(datetime.strptime(col[0], date_format))
        weather.append(col[1])
        temperature.append(col[2])
        pm25.append(col[3])
    
    weatherObj={"Time":time,"weather":weather,"temperature":temperature,"PM2.5":pm25}
    weatherdf= pd.DataFrame(weatherObj)
    weatherdf['Time'] = weatherdf['Time'].dt.floor('Min')
    return weatherdf
#readin order 
def generateOrderDF(date):
    filename="Orders/order_data_"+date
    f= open(filename,"r")
    filedata=f.read()
    rows=filedata.splitlines()
    order_id=[]
    driver_id=[]
    passenger_id=[]
    start_region_hash=[]
    dest_region_hash=[]
    Price=[]
    Time=[]
    for row in rows:
        col=row.split("\t")
        order_id.append(col[0])
        driver_id.append(col[1])
        passenger_id.append(col[2])
        start_region_hash.append(col[3])
        dest_region_hash.append(col[4])
        Price.append(col[5])
        Time.append(datetime.strptime(col[6], date_format))

    OrderObj={
        "order_id":order_id,
        "driver_id":driver_id,
        "passenger_id":passenger_id,
        "start_region_hash":start_region_hash,
        "dest_region_hash":dest_region_hash,
        "Price":Price,
        "Time":Time
    }
    return pd.DataFrame(OrderObj)
# reading region file
def generateRegionDF():
    f= open("cluster_map","r")
    filedata=f.read()
    rows=filedata.splitlines()
    region_hash=[]
    region_id=[]
    for row in rows:
        col=row.split("\t")
        region_hash.append(col[0])
        region_id.append(col[1])

    regionObj={
        "region_hash":region_hash,
        "region_id":region_id
        }
    return  pd.DataFrame(regionObj)
#readin poi data
def generatePoiDF():
    f= open("poi_data","r")
    filedata=f.read()
    rows=filedata.splitlines()
    region_hash=[]
    poi_class=[]
    for row in rows:
        col=row.split("\t")
        region_hash.append(col[0])
        del col[0]
        poi_class.append(col)
    poiObj={
       "region_hash":region_hash,
       "poi_class":poi_class
        }
    return pd.DataFrame(poiObj)
#creating time slots
def createTimeSlots(joinedDF,date):
    print("Creating time slots")
    print(joinedDF)
    timeslots=[]
    date_string = date+' 00:00:00'
    weatherDF=generateWeatherDF(date)
    start = datetime.strptime(date_string, date_format)
    new_time = start
    a=0
    while(new_time.day==start.day):
       a+=1
       timeslots.append(new_time)
       new_time = new_time+ timedelta(minutes=10)
    regionID=1
    while(regionID<67):
     timeIndex=0
     totalreq=[0]
     accpetreq=[0]
     rejreq=[0]
     
     gap=[]
     iarr=[]
     jarr=[]
     
     for index, row in joinedDF[joinedDF["region_id"]==str(regionID)].iterrows():
        
        if timeIndex<=142 and row["Time"]>=timeslots[timeIndex+1]:
            totalreq.append(0)
            accpetreq.append(0)
            rejreq.append(0)
            timeIndex+=1
        else:
            totalreq[timeIndex]+=1
            if row["driver_id"]=="NULL":
               rejreq[timeIndex]+=1
            else : accpetreq[timeIndex]+=1 
     print(date)
     print(regionID)
     leng=(len(accpetreq))   
     
     if leng<144:
         for i in range(144-leng):
             totalreq.append(0)
             accpetreq.append(0)
             rejreq.append(0)

     for i in range(144):
        gap.append(accpetreq[i]-rejreq[i])
        iarr.append(regionID)
        jarr.append(i+1)
     
     counts={
        "TimeSlot":timeslots,
        "i":iarr,
        "j":jarr,
        "Total Requests":totalreq,
        "AcceptedCount":accpetreq,
        "RejectedCount":rejreq,
        "Gapij":gap,
        }
     
     count= pd.DataFrame(counts)
     countjoin=pd.merge(count, weatherDF, left_on='TimeSlot', right_on='Time', how='left').drop(columns=['Time'])
     filename="TimeCounts/"+date+"/count-table-R"+str(regionID)+".csv"
     countjoin.to_csv(filename, index=False)
     regionID+=1
    print("Timeslots created")

