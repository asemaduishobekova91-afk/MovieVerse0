from fastapi import APIRouter
from pydantic import BaseModel
import joblib
from pathlib import Path

from pyexpat import features



BASE_DIR = Path(__file__).resolve().parent
scaler = joblib.load(BASE_DIR / "scaler.pkl")
model = joblib.load(BASE_DIR / "model.pkl")

predict_router = APIRouter(prefix='/predict', tags = ['Predict Price'])

class HousePredictSchema(BaseModel):
    GrLivArea: int
    YearBuilt: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    OverallQual: int
    Neighborhood: str


@predict_router.post('/')
async def predict_price(house: HousePredictSchema):
    house_dict = house.dict()



    new_neighborhood = house_dict.pop('Neighborhood')
    neighborhood1_0 = [
        1 if new_neighborhood == 'Blueste' else 0,
        1 if new_neighborhood == 'BrDale' else 0,
        1 if new_neighborhood == 'BrkSide' else 0,
        1 if new_neighborhood == 'ClearCr' else 0,
        1 if new_neighborhood == 'CollgCr' else 0,
        1 if new_neighborhood == 'Crawfor' else 0,
        1 if new_neighborhood == 'Edwards' else 0,
        1 if new_neighborhood == 'Gilbert' else 0,
        1 if new_neighborhood == 'IDOTRR' else 0,
        1 if new_neighborhood == 'MeadowV' else 0,
        1 if new_neighborhood == 'Mitchel' else 0,
        1 if new_neighborhood == 'NAmes' else 0,
        1 if new_neighborhood == 'NPkVill' else 0,
        1 if new_neighborhood == 'NWAmes' else 0,
        1 if new_neighborhood == 'NoRidge' else 0,
        1 if new_neighborhood == 'NridgHt' else 0,
        1 if new_neighborhood == 'OldTown' else 0,
        1 if new_neighborhood == 'SWISU' else 0,
        1 if new_neighborhood == 'Sawyer' else 0,
        1 if new_neighborhood == 'SawyerW' else 0,
        1 if new_neighborhood == 'Somerst' else 0,
        1 if new_neighborhood == 'StoneBr' else 0,
        1 if new_neighborhood == 'Timber' else 0,
        1 if new_neighborhood == 'Veenker' else 0,

    ]

    features = list(house_dict.values()) + neighborhood1_0
    scaled_data = scaler.transform([features])
    pred = model.predict(scaled_data)[0]
    return {'Price': round(float(pred), 2)}