from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from domain.facade import PredictFacade
from containers_config import PredictContainer

router = APIRouter(prefix="/training")


class Measurement(BaseModel):
    diagnosis: str
    id_number: float
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float


class Prediction(BaseModel):
    id_number: float
    diagnosis: float


class PredictResponse(BaseModel):
    measurements: List[Prediction]


class PredictRequest(BaseModel):
    measurements: List[Measurement]


@router.post("/predict",
             summary="",
             description="",
             response_model=PredictResponse)
@inject
async def predict(request: PredictRequest,
                  run_name: str,
                  predicting_facade: PredictFacade = Depends(
                      Provide[PredictContainer.predicting_facade])) -> PredictResponse:
    prediction = predicting_facade.predict(measurements=[m.dict() for m in request.measurements],
                                           run_name=run_name)
    prediction = prediction.astype(
        {col: 'float64' for col in prediction.select_dtypes('int64').columns})
    prediction = prediction.to_dict(orient="index")
    result = []
    for key in prediction.keys():
        result.append(prediction[key])
    return PredictResponse(measurements=result)
