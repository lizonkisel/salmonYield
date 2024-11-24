"""Module with DPI conteiners"""
from dependency_injector import containers, providers

from src.services.salmon_process import ProcessSalmonImage, Storage
from src.services.preprocess_utils import DiseasePredictor


class Container(containers.DeclarativeContainer):
    """Container for DPI plates"""
    config = providers.Configuration()

    store = providers.Singleton(
        Storage,
        config=config.content_process,
    )

    disease_predictor = providers.Singleton(
        DiseasePredictor,
        config=config.plate_model_parameters,
    )

    content_process = providers.Singleton(
        ProcessSalmonImage,
        storage=store.provider(),
        plate_predictor=disease_predictor.provider(),
    )
