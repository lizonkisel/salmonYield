"""Module for define APP plate process."""

import typing as tp
from pathlib import Path
import sqlite3
import time
import cv2
import numpy as np

from src.services.preprocess_utils import DiseasePredictor


class Storage:
    """Class for storing processed results"""
    def __init__(self, config: dict):
        self._config = config
        self._db_conn = sqlite3.connect(self._config.db_path)
        cursor = self._db_conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL
            )
            """,
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS measurements_data (
                measurements_data_id INTEGER NOT NULL,
                parameter TEXT NOT NULL,
                value TEXT,
                FOREIGN KEY(measurements_data_id) REFERENCES measurements(id)
            )
            """,
        )
        self._db_conn.commit()

    def get(
            self,
            group_id: str,
            from_ts: int = 0,
            to_ts: int = 0,
    ) -> dict:
        now = time.time()
        if from_ts > now or to_ts < from_ts:
            return {
                "code": 400,
                "data": {},
                "error": 'INVALID TIME',
            }

        if to_ts == 0:
            to_ts = int(now + 1)
        limit = 1000
        if from_ts != 0:
            limit = int((to_ts - from_ts) / 86400)  # seconds/day

        if limit < 1 or limit > 1000:
            return {
                "code": 422,
                "data": {},
                "error": 'INVALID DATA LIMIT',
            }

        custom_response = {
            "code": 500,
            "data": {},
            "error": 'CAN NOT GET DATA',
        }
        number_of_roperties = 18
        cursor = self._db_conn.cursor()
        cursor_data = cursor.execute(
            """
                SELECT m.id, m.timestamp, d.parameter, d.value FROM
                    measurements m
                    JOIN measurements_data d ON (m.id = d.measurements_data_id)
                WHERE m.timestamp < ?
                ORDER BY m.id DESC
                LIMIT ?
                """,
            (to_ts, limit * number_of_roperties),
        )

        python_db_structure = {}
        for row in cursor_data:
            if row[2] not in python_db_structure:
                python_db_structure[row[2]] = [
                    {
                        'id': int(row[0]),
                        'timestamp': int(row[1]),
                        'value': float(row[3]),
                    }
                ]
            else:
                python_db_structure[row[2]].append(
                    {
                        'id': int(row[0]),
                        'timestamp': int(row[1]),
                        'value': float(row[3]),
                    }
                )
        cursor_data.close()

    def put(
            self,
            content_json: dict,
    ) -> dict:
        custom_response = {
            "code": 200,
            "data": {},
            "error": "No errors",
        }
        now = time.time()
        input_ts = content_json['dateStart']
        if (
                input_ts != content_json['dateFinish']
                or input_ts > now
                or input_ts == 0
        ):
            input_ts = int(now + 1)

        cursor = self._db_conn.cursor()
        cursor.execute(
            """
            INSERT INTO measurements (timestamp) VALUES (?) RETURNING id
            """, (input_ts, )
        )
        measurement_id = cursor.fetchone()[0]
        for parameter in content_json:
            if parameter not in ['dateStart', 'dateFinish']:
                value = content_json[parameter]
                cursor.execute(
                    """
                    INSERT INTO measurements_data (
                        measurements_data_id,
                        parameter,
                        value
                    ) VALUES (?, ?, ?)
                    """, (measurement_id, str(parameter), value))
        self._db_conn.commit()
        return custom_response

    def save_hard(
            self,
            image: np.ndarray,
            image_name: str,
            image_ts: int,
    ) -> None:
        image_path = Path(self._config["dir_path"]) / f"{image_ts}_{image_name}.jpg"
        _ = cv2.imwrite(
            str(image_path),
            image
        )


class ProcessSalmonImage:
    """Class for storing processed"""
    status = "Start process image first"

    def __init__(
        self,
        storage: Storage,
        salmon_disease_predictor: DiseasePredictor
    ):
        self.storage = storage
        self.granules_mask_predictor = salmon_disease_predictor

    def process(
            self,
            image: np.ndarray,
            content_name: str,
            content_ts: int,
    ) -> dict:
        self.storage.save_hard(image, content_name, content_ts)
        is_salmon_diseased = self.granules_mask_predictor.predict(
            image,
        )
        return {
            "code": 200,
            "data": {'predicted_disease': is_salmon_diseased},
            "error": "No errors",
        }
