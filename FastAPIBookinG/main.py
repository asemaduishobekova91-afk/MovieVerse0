from fastapi import FastAPI
from shop_app.admin.setup import setup_admin
from shop_app.api import user,country,hotel,hotel_image,city,room,room_image,booking,review,auth
import uvicorn


shop_app = FastAPI(title='Booking')
shop_app.include_router(user.user_router)
shop_app.include_router(country.country_router)
shop_app.include_router(hotel.hotel_router)
shop_app.include_router(hotel_image.hotel_image_router)
shop_app.include_router(city.city_router)
shop_app.include_router(room.room_router)
shop_app.include_router(room_image.room_image_router)
shop_app.include_router(booking.booking_router)
shop_app.include_router(review.review_router)
shop_app.include_router(auth.auth_router)
setup_admin(shop_app)


if __name__ == '__main__':
    uvicorn.run(shop_app, host='127.0.0.1', port=8003)