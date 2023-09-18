from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
import datetime as dt

booking_router = APIRouter()
uri = "mongodb+srv://sannithnalluri2003:Collabwave1@cluster0.dp7lisq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['Bike_details_database']
collection = db['Bike_details']
upcomingcollection = db['AlreadyBooking']



BookedRecord = []
def bike_currently_not_booked(pickup_date, pick_time, plan, bikedata):
    pickupdata_time = datetime.strptime(pickup_date + ' ' + pick_time, '%Y-%m-%d %H:%M:%S')

    print(bikedata['bikename'])
    AlreadyBookedRecords = upcomingcollection.find({})
  
    
    if AlreadyBookedRecords:
        for Records in AlreadyBookedRecords:
            Records['_id'] = str(Records["_id"])
            BookedRecord.append(Records)

    print(BookedRecord)
 


@booking_router.get('/Shsssowavaible_bike')
async def Showavaible_bike(pickupdata: str, pickuptime: str, plan: str):
    # Send the details of bikes which are not booked
    BikeData = collection.find({})
    bike_list = []
    for Bike in BikeData:
        if Bike['bikebookingstatus']  == 'false':
           res =bike_currently_not_booked(pickupdata,pickuptime,plan,Bike)

        return {'api connection sucessfull'}

















    # # Send the details of bikes which have expiry times less than the pickup data and time  
    # All_bike_data = collection.find({})
    # for bike in All_bike_data:
    #     if bike['bikebookingstatus'] == True:
    #         if isinstance(bike['currentexpirytime'], str):
    #             bike_expiry_date = datetime.strptime(bike['currentexpirytime'], '%Y-%m-%d %H:%M:%S')
    #         elif isinstance(bike['currentexpirytime'], datetime):
    #             bike_expiry_date = bike['currentexpirytime']
    #         pickupdateandtime = datetime.strptime(pickupdata + ' ' + pickuptime, '%Y-%m-%d %H:%M:%S')

    #         # Check if the pickup datetime is greater than or equal to the bike's expiry datetime
    #         if pickupdateandtime >= bike_expiry_date:
    #             print('Bike is available')
    #             bike['_id'] = str(bike['_id'])
    #             bike_list.append(bike)
    #         else:
    #             print('Bike is not available')

    #     # Check whether the current expiry date is less than booked bikes' pickup date then show    
    #     plannumber = int(plan)
    #     print(plannumber)
    #     if plannumber == 3:
    #         plan_duration = dt.timedelta(hours=3)
    #     elif plannumber == 5:
    #         plan_duration = dt.timedelta(hours=5)
    #     elif plannumber == 7:
    #         plan_duration = dt.timedelta(hours=7)
    #     elif plannumber == 24:
    #         plan_duration = dt.timedelta(hours=24)
    #     elif plannumber == 2:  # Handle the 2-minute plan
    #         plan_duration = dt.timedelta(minutes=2)

    #     end_time = pickupdateandtime + plan_duration

    # Already_booked_bike_data = upcomingcollection.find({})
    # for Abike in Already_booked_bike_data:
    #     pickuplanneddate = Abike['pickuptime']
    #     pickuplanneddate_time = datetime.strptime(pickuplanneddate, '%Y-%m-%d %H:%M:%S')
    #     print(pickuplanneddate)
    #     if end_time <= pickuplanneddate_time:
    #         bike['_id'] = str(bike['_id'])
    #         bike_list.append(bike)
    #     else:
    #         print('current endtime:', end_time)
    #         print('pickup', pickuplanneddate)
    #         print('bike cannot be booked')

  

@booking_router.get('/get_bike_details')
async def get_bike_details(bikeId: str):
    try:
        id = ObjectId(bikeId)
        bike_details = collection.find_one({"_id": id})

        if bike_details is None:
            raise HTTPException(status_code=404, detail="Bike not found")

        # Convert ObjectId to string for JSON serialization
        bike_details["_id"] = str(bike_details['_id'])

        # Create a list containing the bike details
        bikedata = [bike_details]

        return bikedata
    except Exception as e:
        # Handle other exceptions or errors here
        raise HTTPException(status_code=500, detail="Internal Server Error")
