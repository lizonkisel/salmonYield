"""Model with preprocessing utilities"""


import typing as tp

import cv2
import numpy as np
import onnxruntime as ort

# from src.services.salmon_utils import matrix_to_string

BATCH_SIZE = 1
PROVIDERS = (
    'CUDAExecutionProvider',
    "CPUExecutionProvider",
)


class DiseasePredictor:
    def __init__(self, config: dict):
        # Инициализировали один раз и сохранили в атрибут
        self.ort_session = ort.InferenceSession(
            config.granules_checkpoint,
            providers=PROVIDERS,
        )
        self.image_size = (
            config.granules_img_width,
            config.granules_img_height,
        )

    def onnx_preprocessing(
        self,
        image: np.ndarray,
        image_size: tp.Tuple[int, int] = (512, 512),
    ) -> np.ndarray:
        image = cv2.resize(image.copy(), image_size, interpolation=cv2.INTER_LINEAR)
        mean = np.array((0.485, 0.456, 0.406), dtype=np.float32) * 255.0
        std = np.array((0.229, 0.224, 0.225), dtype=np.float32) * 255.0
        denominator = np.reciprocal(std, dtype=np.float32)
        image = image.astype(np.float32)
        image -= mean
        image *= denominator
        return image.transpose((2, 0, 1))[None]

    def predict(
        self,
        image: np.ndarray,
    ) -> tp.Tuple[np.array, np.array]:
        onnx_input = self.onnx_preprocessing(image, image_size=self.image_size)
        onnx_input = np.concatenate([onnx_input] * BATCH_SIZE)
        ort_inputs = {self.ort_session.get_inputs()[0].name: onnx_input}
        ort_outputs = self.ort_session.run(None, ort_inputs)[0]
        pr_mask = ort_outputs.squeeze().round()
        return image, pr_mask.astype(np.uint8)