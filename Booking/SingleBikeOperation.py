from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId

singleBike_router = APIRouter()
uri = "mongodb+srv://sannithnalluri2003:Collabwave1@cluster0.dp7lisq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['Bike_details_database']
collection = db['Bike_details']
upcomingcollection = db['AlreadyBooking']

@singleBike_router.get('/get_single_bike_data')
def get_single_bike_data(bike_id:str):
    bike_data = collection.find_one({'_id':ObjectId(bike_id)})
    bike_data['_id'] = str(bike_data['_id'])
    return bike_data