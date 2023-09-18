from fastapi import FastAPI
from Booking.BikeDetails import BikeDetailsRouter
from Booking.DisplayBike import booking_router
from Booking.BookingDetails import Bookbike_router
from Booking.AdminBikeControl import Admin_router
from fastapi.middleware.cors import CORSMiddleware
from Booking.BookingbikeDisplay import BikeBooking_router
from Booking.ShowAvaiable import ShowAvaiable_router
app = FastAPI()
app.include_router(BikeDetailsRouter)
app.include_router(booking_router)
app.include_router(Admin_router)
app.include_router(Bookbike_router)
app.include_router(BikeBooking_router)
app.include_router(ShowAvaiable_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use "*" to allow all origins (not recommended for production)
    allow_methods=["*"],  # Use "*" to allow all HTTP methods
    allow_headers=["*"],  # Use "*" to allow all headers
    allow_credentials=True,  # Allow credentials (e.g., cookies)
    expose_headers=["*"],  # Use "*" to expose all headers
)