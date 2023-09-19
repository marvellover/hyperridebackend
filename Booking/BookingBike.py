from fastapi import APIRouter, UploadFile, File
from pymongo import MongoClient
from datetime import datetime
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger 
from bson import ObjectId


Bookingbike_router=APIRouter()
scheduler = BackgroundScheduler()
scheduler.start()

uri2 = "mongodb+srv://sannithnalluri2003:Collabwave1@cluster0.dp7lisq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri2)
db = client['Bike_details_database']
collection = db['Bike_details']
upcomingcollection = db['AlreadyBooking']
bookingrecords = db['bikebookingrecords']

def bookthebike(pickup,endtime):
    dict = {
       'pickup':pickup,
       'endtime':endtime
    }
    res = bookingrecords.insert_one(dict)
    print('successfully booked')
    return {'succesfully bookeed'}

@Bookingbike_router.get('/bookbikenowresting')
def bookbikenow(pickupdataandtime,enddataandtime):
    pickup = datetime.strptime(pickupdataandtime,'%Y-%m-%d %H:%M:%S') 
    endtime = datetime.strptime(enddataandtime,'%Y-%m-%d %H:%M:%S') 

    #scheduler.add_job(bookbikenow,args=[pickup,endtime],trigger=pickupdataandtime)
    scheduler.add_job(periodic_task, 'interval', seconds =10)
    return 'message triger'
def periodic_task():
    try:
       testcollection = db['tesing']
       testcollection.insert_one({'count ':10})
       
    except Exception:
       print('exception')
    # Your periodic task code here

# Schedule a periodic task
   
# Shutdown the scheduler when the FastAPI app stops
@Bookingbike_router.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()