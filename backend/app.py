"""Main module for FastAPI salmon-yield backend service."""
import argparse

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from omegaconf import OmegaConf

from src.containers.containers import Container
from src.routes import salmon as plates_routes
from src.routes.routers import router as app_router


def create_app() -> FastAPI:
    """
    Create FastAPI application with DPI Containers
    :return: FastAPI application
    """
    container = Container()
    cfg = OmegaConf.load("configs/config.yaml")
    container.config.from_dict(cfg)
    container.wire([plates_routes])

    app = FastAPI(
        title=cfg['title'],
        description=(
            "Salmon-Yield API. "
            "You can: "
            "get salmon data according to its group number and date;"
            "save new data with/without new group."
        ),
        summary=cfg['summary'],
        version=cfg['version'],
        terms_of_service=cfg['terms_of_service'],
        contact=cfg['contact'],
        license_info=cfg['license_info'],
    )
    app.include_router(app_router, tags=["salmon-groups"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    return app


if __name__ == "__main__":

    def arg_parse():
        """
        Parse command line
        :return: dictionary with command line arguments
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("port", type=int, help="port number")
        return parser.parse_args()

    app = create_app()
    args = arg_parse()
    uvicorn.run(app, port=args.port, host="127.0.0.1")
