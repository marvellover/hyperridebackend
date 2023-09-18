from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId

Admin_router = APIRouter()
uri = "mongodb+srv://sannithnalluri2003:Collabwave1@cluster0.dp7lisq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['Bike_details_database']
collection = db['Bike_details']
upcomingcollection = db['AlreadyBooking']

@Admin_router.get('/All_bike_data')
async def All_bike_data():
    return None

@Admin_router.post('/Update_booking_details')
async def Update_the_bike_details(bike_id:str):
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
            return(f'Successfully updated  times for bike ID {id}')
        else:
            return(f'Failed to update bike details for bike ID {id}')
    except Exception as e:
        print('Error:', str(e))


@Admin_router.post('/del_the_upcoming_booking')
async def del_the_upcoming_booking(id: str):
    print('The bike_id', id, 'is trigerred to deleted from upcoming booking')
    try:
        res = upcomingcollection.delete_one({'_id': ObjectId(id)})
        if res.deleted_count > 0:
            print('Successfully deleted from upcoming booking')
            return {'message': "Successfully deleted the record with id " + id}
        else:
            print('No data found with id ', id)
            return {'message': 'No data found with this id ' + id}
    except Exception as e:
        print(e)
        return {'message': 'An error occurred while deleting the record'}

# Assuming that "upcomingcollection" is your MongoDB collection.


@Admin_router.get('/get_all_future_bookin_detials')
async def get_all_future_bookin_detials():
    Bookingdata = upcomingcollection.find({})
    data =[]
    for booking in Bookingdata:
        booking['_id'] = str(booking['_id'])
        data.append(booking)
    return data


@Admin_router.get('/get_all_advancce_booking')
def get_all_advancce_booking():
    upcomingcollection.delete_many({})
    return{'message the deleted all advance Booking'}