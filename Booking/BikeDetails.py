from fastapi import APIRouter, UploadFile, File
from pymongo import MongoClient
from pydantic import BaseModel
import cloudinary
from cloudinary.uploader import upload

# Configure the Cloudinary details for image uploads
cloudinary.config(
    cloud_name="dwuvtxmcr",
    api_key="117689382957923",
    api_secret="l3B5zzSPpWwflawMhafxg43OfKQ"
)

# Configure the MongoDB server details
uri = "mongodb+srv://sannithnalluri2003:Collabwave1@cluster0.dp7lisq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['Bike_details_database']
collection = db['Bike_details']

BikeDetailsRouter = APIRouter()

# class BikeDetailsModel(BaseModel):
#     bikename: str
#     bikebookingstatus: bool
#     currentpickuptime: str
#     currentexpirytime: str
#     bikeFeatures1: str
#     bikeFeatures2: str
#     bikeFeatures3: str
#     bikeImage: UploadFile = File(...)

# Create your FastAPI endpoint
@BikeDetailsRouter.post('/Upload_bike_details')
async def upload_bike_details(
    bikename: str,
    bikebookingstatus: bool,
    currentpickuptime: str,
    currentexpirytime: str,
    bikeFeatures1: str,
    bikeFeatures2: str,
    bikeFeatures3: str,
    bikeImage: UploadFile = File(...)):
    # Upload the image to Cloudinary
    response = upload(bikeImage.file, folder='Bikeimages')
    image_url = response['secure_url']

    # Create a dictionary with bike details
    bike_details = {
        "bikename": bikename,
        "bikebookingstatus": bikebookingstatus,
        "currentpickuptime": currentpickuptime,
        "currentexpirytime": currentexpirytime,
        "bikeFeatures1": bikeFeatures1,
        "bikeFeatures2": bikeFeatures2,
        "bikeFeatures3": bikeFeatures3,
        "bikeImage": image_url
    }

    # Insert the bike details into MongoDB
    collection.insert_one(bike_details)

    return {'message': 'Successfully Uploaded Bike Details'}

@BikeDetailsRouter.get('/Get_all_bike_details')
async def Get_all_bike_details():
    BikeData = collection.find({})
    bike_list = []
    for bike in BikeData:
        bike['_id'] = str(bike['_id'])
        bike_list.append(bike)
    return bike_list
