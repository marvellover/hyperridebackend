from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import datetime as dt


ShowAvaiable_router = APIRouter()
uri = "mongodb+srv://sannithnalluri2003:Collabwave1@cluster0.dp7lisq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['Bike_details_database']
collection = db['Bike_details']
upcomingcollection = db['AlreadyBooking']


pickupdataandtime = None
endtime = None
avaliblebikeId = []


@ShowAvaiable_router.get('/get_the_avaiable_bike_data')
def get_the_avaiable_bike_data(pickuptime:str,plan:str):
    avaliblebikeId = []
    #converting pickuptime to dateandtime
    pickupdatetime =datetime.strptime(pickuptime,'%Y-%m-%d %H:%M:%S')
    
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

    All_bike_records = collection.find({})

    for bike_record in All_bike_records:
     if bike_record['bikebookingstatus'] == False:
        # The bike is not currently booked, checking if it's in the upcoming booking list
        bike_id = str(bike_record['_id'])
        Advance_booking_records = upcomingcollection.find({})
        bike_id_found = False  # Initialize the flag as False

        for bike_record in All_bike_records:
            if bike_record['bikebookingstatus'] == False:
        # The bike is not currently booked, checking if it's in the upcoming booking list
              bike_id = str(bike_record['_id'])
              Advance_booking_records = upcomingcollection.find({})
              bike_id_found = False  # Initialize the flag as False

              for A_booking_record in Advance_booking_records:
                if A_booking_record['bike_id'] == bike_id:
                    print('The bike is in the upcoming booking', bike_id)

                # Now, check if pickuptime is greater than the provided end_time
                    pickuptime_str = A_booking_record.get('pickuptime', '')
                    if pickuptime_str:
                        pickuptime = datetime.fromisoformat(pickuptime_str)
                        if pickuptime > end_time:
                            print('Yes, pickuptime is greater than the provided end_time')
                            avaliblebikeId.append(bike_id)
                        else:
                            print('No, pickuptime is not greater than the provided end_time')
                    else:
                        print('No pickuptime data found in the booking record')

                    bike_id_found = True  # Set the flag to True
                    break  # No need to continue searching, we found it
              if not bike_id_found:
                print('The bike is not in the upcoming list')
                avaliblebikeId.append(bike_id)
            else:
               print('Bike is currently booked')

    return avaliblebikeId