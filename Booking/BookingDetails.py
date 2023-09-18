from fastapi import APIRouter, UploadFile, File
from pymongo import MongoClient
from datetime import datetime
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger 
from bson import ObjectId

Bookbike_router=APIRouter()
scheduler = BackgroundScheduler()
scheduler.start()

uri2 = "mongodb+srv://sannithnalluri2003:Collabwave1@cluster0.dp7lisq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri2)
db = client['Bike_details_database']
collection = db['Bike_details']
upcomingcollection = db['AlreadyBooking']



def book_bike_background(bike_id,endtime,pickuptime):
   id = ObjectId(bike_id)
   try:
        print('Updating booking details for bike ID:', bike_id)
    
        bike_intial_details = collection.find_one({'_id':id})
        print(bike_intial_details)

        end_time = endtime +dt.timedelta(minutes=30)
        updated_bike_details = {
            "bikebookingstatus": True,
            "currentpickuptime": pickuptime,
            "currentexpirytime": end_time,
        }

        # Update the bike details in MongoDB
        result = collection.update_one({"_id": id}, {"$set": updated_bike_details})

        if result.modified_count == 1:
            print(f'Successfully updated booking status and pickup times for bike ID {id}')
        else:
            print(f'Failed to update bike details for bike ID {id}')
   except Exception as e:
        print('Error:', str(e))

def relese_bike_background(bike_id):
   id = ObjectId(bike_id)
   try:
        print('Updating booking details for bike ID:', bike_id)
    
        updated_bike_details = {
            "bikebookingstatus": False,
            "currentpickuptime": '0000-00-00 00:00:00',
            "currentexpirytime": '0000-00-00 00:00:00',
        }

        # Update the bike details in MongoDB
        result = collection.update_one({"_id": id}, {"$set": updated_bike_details})

        if result.modified_count == 1:
            print(f'Successfully updated  times for bike ID {id}')
        else:
            print(f'Failed to update bike details for bike ID {id}')
   except Exception as e:
        print('Error:', str(e))
  
def del_the_upcoming_booking(id: str):
    print('The bike_id', str(id), 'is trigerred to deleted from upcoming booking')
    try:
        res = upcomingcollection.delete_one({'_id': ObjectId(id)})
        if res.deleted_count > 0:
            print('Successfully deleted from upcoming booking')
            return {'message': "Successfully deleted the record with id " + str(id)}
        else:
            print('No data found with id ', str(id))
            return {'message': 'No data found with this id ' + str(id)}
    except Exception as e:
        print(e)
        return {'message': 'An error occurred while deleting the record'}



@Bookbike_router.get('/BookBike')
async def Book_bike(pickuptime: str, plan: str,bike_id :str):
    try:
        plannumber = int(plan)
        # Parse the pickuptime string to a datetime object
        pickuptime_datetime = datetime.strptime(pickuptime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return {"error": "Invalid pick-up time format. Use 'YYYY-MM-DD HH:MM:SS'"}

    # Calculate the end time based on the selected plan
    if plannumber == 3:
        plan_duration = dt.timedelta(hours=3)
    elif plannumber == 5:
        plan_duration = dt.timedelta(hours=5)
    elif plannumber == 7:
        plan_duration = dt.timedelta(hours=7)
    elif plannumber == 24:
        plan_duration =dt.timedelta(hours=24)
    elif plannumber == 2:  # Handle the 2-minute plan
        plan_duration = dt.timedelta(minutes=2)
    

    endtime = pickuptime_datetime + plan_duration
    ExpireData_time = endtime.strftime('%Y-%m-%d %H:%M:%S')
    

    BookedRecord = {
        'bike_id':bike_id,
        'pickuptime':pickuptime,
        'endtime':endtime
    }
    try:
        res = upcomingcollection.insert_one(BookedRecord)
        print('Inserted document ID:', res.inserted_id)
        doucment_id= res.inserted_id
    except Exception as e:
        print('An error occurred during insertion:', e)

    scheduler.add_job(
        del_the_upcoming_booking,
        trigger=DateTrigger(run_date=pickuptime_datetime),
        args=[doucment_id],
        id='remove upcoming_job',
        replace_existing=True
    )
    scheduler.add_job(
        book_bike_background,
        trigger=DateTrigger(run_date=pickuptime_datetime),  
        args=[bike_id, endtime, pickuptime],
        id="book_bike_job",
        replace_existing=True,
    )


    scheduler.add_job(
        relese_bike_background,
        trigger=DateTrigger(run_date=ExpireData_time),
        args=[bike_id],
        id='Bike_relese',
        replace_existing=True

    )
    print('trigger is generated')


    # You can return the booking details here
    return {
        "message": "Successfully booked bike",
        "pickuptime": pickuptime_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        "endtime": endtime.strftime('%Y-%m-%d %H:%M:%S'),
        "duration_hours": plannumber,
    }



@Bookbike_router.get('/get_booking_data')
def get_booking_data(pickuptime:str,plan:str):
     try:
        plannumber = int(plan)
        # Parse the pickuptime string to a datetime object
        pickuptime_datetime = datetime.strptime(pickuptime, '%Y-%m-%d %H:%M:%S')
     except ValueError:
        return {"error": "Invalid pick-up time format. Use 'YYYY-MM-DD HH:MM:SS'"}

    # Calculate the end time based on the selected plan
     if plannumber == 3:
        plan_duration = dt.timedelta(hours=3)
        cost = 149
     elif plannumber == 5:
        plan_duration = dt.timedelta(hours=5)
        cost = 220
     elif plannumber == 7:
        plan_duration = dt.timedelta(hours=7)
        cost = 280
     elif plannumber == 24:
        plan_duration =dt.timedelta(hours=24)
        cost = 399
     elif plannumber == 2:  # Handle the 2-minute plan
        plan_duration = dt.timedelta(minutes=2)
    

     endtime = pickuptime_datetime + plan_duration
     ExpireData_time = endtime.strftime('%Y-%m-%d %H:%M:%S')

     return endtime,cost
 