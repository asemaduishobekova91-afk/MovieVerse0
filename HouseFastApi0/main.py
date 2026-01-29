from fastapi import FastAPI
import uvicorn
from house_app.api import users,region,city,district,property,images,reviews,auth
from house_app.admin.setup import setup_admin
from house_app.api import predict

house_app = FastAPI(title='House.kg')
house_app.include_router(users.users_router)
house_app.include_router(region.region_router)
house_app.include_router(city.city_router)
house_app.include_router(district.district_router)
house_app.include_router(property.property_router)
house_app.include_router(images.images_router)
house_app.include_router(reviews.reviews_router)
house_app.include_router(auth.auth_router)
setup_admin(house_app)
house_app.include_router(predict.predict_router)





if __name__ == '__main__':
    uvicorn.run(house_app, host='127.0.0.1', port=8003)