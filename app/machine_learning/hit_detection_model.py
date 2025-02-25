import os

from ultralytics import YOLO

from app.machine_learning.base_model import DetectionModel


class HitDetectionModel(DetectionModel):
    _best_weights = os.path.join(
        os.path.dirname(__file__),
        "resources/hit_weights.pt",
    )
    _model = best_model = YOLO(_best_weights, task="detect")

    def detect(self, image_paths):
        self.results = self._model(image_paths, iou=0.5)
        return self.results
