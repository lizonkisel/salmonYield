"""Module for FastAPI requests infrastructure"""

import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, File, UploadFile
from pydantic import BaseModel

from src.containers.containers import Container
from src.routes.routers import router
from src.services.salmon_process import ProcessSalmonImage, Storage


@router.get("/get_salmon_group")
@inject
def get_content(
    group_id: str,
    from_ts: int = 0,
    to_ts: int = 0,
    storage: Storage = Depends(Provide[Container.store]),
) -> dict:
    """
    Define GET content
    :param group_id: group name of salmon
    :param storage: container with storage functionality
    :return: dict with content
    """
    custom_response = storage.get(group_id, from_ts, to_ts)
    return custom_response


class SalmonGroup(BaseModel):
    groupElem: str
    dateStart: int
    dateFinish: int
    temperature: float
    NH4: float
    NO2: float
    pH: float
    Kh: float
    CO2: float
    amount: int
    biomass: float
    averMass: float
    breed: str
    gender: bool
    feedStandartPercent: float
    feedStrategy: float
    realStandart: float
    feedStandartMass: float
    feedSize: float
    deathAmount: int
    deathPercent: float


@router.post("/set_salmon_group")
@inject
def process_content(
    content_json: SalmonGroup,
    storage: Storage = Depends(Provide[Container.store]),
) -> dict:
    """
    Define POST
    :param content_json: input json with new salmon group data
    :param content_process: container with process functionality
    :return: dictionary with results in json format
    """
    custom_response = storage.put(content_json)
    return custom_response


class SalmonImage(BaseModel):
    content_image: UploadFile = File(
        ...,
        title="PredictorInputImage",
        alias="image",
        description="Image with fish for disease prediction.",
    )
    image_ts: int


@router.post("/predict_disease")
@inject
def process_content(
    content_json: SalmonImage,
    content_process: ProcessSalmonImage = Depends(Provide[Container.content_process]),
) -> dict:
    """
    Define POST
    :param content_image: input image
    :param content_process: container with process functionality
    :return: dictionary with results in json format
    """
    content_image = content_json['content_image']
    image_data = content_image.file.read()
    content_image.file.close()

    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    str_process = content_process.process(
        image,
        str(content_image.filename),
        content_json['image_ts'],
    )
    return {
        "code": 200,
        "data": str_process,
        "error": None,
    }
