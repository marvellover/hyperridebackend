from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
import datetime as dt
import logging

# Configure the logging system
logging.basicConfig(level=logging.DEBUG)  # Set the logging level

# Create a logger instance
logger = logging.getLogger(__name__)

BikeBooking_router = APIRouter()
uri = "mongodb+srv://sannithnalluri2003:Collabwave1@cluster0.dp7lisq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['Bike_details_database']
collection = db['Bike_details']
upcomingcollection = db['AlreadyBooking']

class BikeBooking():

    pickupdataandtime = None
    endtime = None
    avaliblebikeId =[]
    bikeData =[]
    #the funtion for calutating the data and booking time
    @staticmethod
    def bike_booking_calulation(pickupdatetime: datetime, plan: str):
        plannumber = int(plan)
        if plannumber == 3:
            plan_duration = dt.timedelta(hours=3)
        elif plannumber == 5:
             plan_duration = dt.timedelta(hours=5)
        elif plannumber == 7:
             plan_duration = dt.timedelta(hours=7)
        elif plannumber == 24:
            plan_duration = dt.timedelta(hours=24)
        elif plannumber == 2:  # Handle the 2-minute plan
            plan_duration = dt.timedelta(minutes=2)

        end_time = pickupdatetime + plan_duration
        BikeBooking.pickupdataandtime = pickupdatetime
        BikeBooking.endtime = end_time
        return pickupdatetime, end_time, plan_duration

    @staticmethod
    #checking the future booking of bikes
    @staticmethod
    async def check_future_booking(bike_id):
        logger.debug('checking All in future  records')
        sample_id =str(bike_id)  
        logger.debug('currenly checking data for bikeid:',sample_id) 
        result = await get_all_booked_data(sample_id)
        bike_ids =[]
        logger.debug('\n the data of bike fetched in already booked \n')
        enddatetime = BikeBooking.endtime
        logger.debug(enddatetime)

        for res in result:
            pickuptime = res['pickuptime']
            pickupdatetime = datetime.strptime(pickuptime,'%Y-%m-%d %H:%M:%S')
            if enddatetime <=pickupdatetime:
                logger.debug('the current booking time and its expire are',enddatetime,'are less than ',pickupdatetime)
                logger.debug('\n the is append to avalible bike',sample_id)
                BikeBooking.avaliblebikeId.append(sample_id)
            else:
                logger.debug('pritn the current booking expire time ',enddatetime,'is greater than',pickupdatetime)


      

        

    async def list_of_bike_avaliable():
      bike_data = collection.find({})
      for bike in bike_data:
        if bike['bikebookingstatus'] ==False:
            logger.debug(bike['_id'],'are in not currently booked \n')
            notbooked = await check_the_bike_in_booking(bike['_id'])#firstly checking if its not currently booked then future booking
        else:
            logger.debug('\n The bike is in currently booking state',bike['_id'])
            resonse = await BikeBooking.check_the_expiretime(bike['_id'])

    async def check_the_expiretime(id):
        pickuptime = BikeBooking.pickupdataandtime
        logger.debug('the requrie picktime is',pickuptime)
        currenbikedata = collection.find_one({'_id':id})
        expirtydate =currenbikedata['currentexpirytime']
        logger.debug(expirtydate)
        if pickuptime >= expirtydate:
            logger.debug('\n the current_bike pickuptime is',pickuptime,'greater than ',expirtydate)
            BikeBooking.avaliblebikeId.append(id)
            logger.debug("the bike is already booked but its expiry time is mathched with pickup \n")
        else:    
             logger.debug('\n the current_bike pickuptime is',pickuptime,'less than ',expirtydate )
        return

async def get_avaialble_bike_data(unique):
        logger.debug("get bike is called")
        Avaliblebikedata =[]
        Bike_id = unique
        for id in Bike_id:
            logger.debug('avaible bike id are a:',id)
            bikeData = collection.find_one({'_id':ObjectId(id)})
            bikeData['_id'] = str(bikeData['_id'])
            Avaliblebikedata.append(bikeData)
   
        return Avaliblebikedata

async def gererate_uniqueId(bikeid):#function to generate the unqiue id
     unique_id = []
     for id in bikeid:
        if id  in unique_id:
            logger.debug('ID is already in the unique list:', id)        
        else:
            unique_id.append(id)

     return unique_id



### the actual program start here of checking bike data
# the progrma start cheking for the avalible bike

@BikeBooking_router.get('/Showavaible_bike')
async def Showavaible_bike(pickupdate: str, pickuptime: str, plan: str):
    try: 
        logger.debug('\n bike checking started')
        BikeBooking.avaliblebikeId = []
        logger.debug('\n inital avlaibel bike are:',BikeBooking.avaliblebikeId)
        pickupdatetime = datetime.strptime(pickupdate + " " + pickuptime, '%Y-%m-%d %H:%M:%S')

    #calutation the pickuptime and planduration time
        res = BikeBooking.bike_booking_calulation(pickupdatetime, plan)

    #call the list of bike avalible
        avavibelbike = await BikeBooking.list_of_bike_avaliable() 


        all_bike_id=BikeBooking.avaliblebikeId
        unquie_id = await gererate_uniqueId(all_bike_id)
        for id in unquie_id:
            logger.debug('currently avalible bike are:',id)
            bikedata = await get_avaialble_bike_data(unquie_id)
        return bikedata
    except Exception as e:
        return e

#checking firstly that bike id is present in the booking data
@BikeBooking_router.get('/check_the_bike_in_booking')
async def check_the_bike_in_booking(bike_id):
    logger.debug('\n checking for future booking \n')
    id = str(bike_id)
    bookedrecords = upcomingcollection.find({})
    for records in bookedrecords:
        if records['bike_id'] == id:
            logger.debug("the bike is present in future booking checking future booking \n")
            res =await BikeBooking.check_future_booking(id)
        else:
            logger.debug('\n the bike is not in future booking recrord =',bike_id)
            if bike_id not in BikeBooking.avaliblebikeId:
                 BikeBooking.avaliblebikeId.append(bike_id)
                 logger.debug('\n the bike id append to avabile id')
    return 



@BikeBooking_router.get('/get_all_booked_data')
async def get_all_booked_data(bike_id):
    booked = upcomingcollection.find({'bike_id':bike_id})
    bookeddata =[]
    for book in booked:
        book['_id'] = str(book['_id'])
        bookeddata.append(book)
    
    return bookeddata


