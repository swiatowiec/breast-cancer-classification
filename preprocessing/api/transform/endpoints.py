from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from containers_config import TransformContainer
from domain.facade import PreprocessingTransformFacade

router = APIRouter(prefix="/preprocessing")


class Measurement(BaseModel):
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
    compactness_se: float
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
    run_name: str

class PreprocessTransformResponse(BaseModel):
    measurements: List[Measurement]


class PreprocessTransformRequest(BaseModel):
    measurements: List[Measurement]


@router.post("/transform",
             summary="Preprocess measurements",
             description="Preprocess measurements",
             response_model=PreprocessTransformResponse)
@inject
async def transform(request: PreprocessTransformRequest,
                    run_name: str,
                    preprocessing_transform_facade: PreprocessingTransformFacade = Depends(
                        Provide[TransformContainer.preprocessing_transform_facade])) -> PreprocessTransformResponse:
    results = preprocessing_transform_facade.transform(measurements=[m.dict() for m in request.measurements],
                                                       run_name=run_name,
                                                       )
    return PreprocessTransformResponse(measurements=[Measurement.parse_obj(r) for r in results])
