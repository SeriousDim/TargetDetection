import os
import numpy as np
from ultralytics import YOLO

class DetectionModel:
    _best_weights = os.path.join(os.path.dirname(__file__), "resources/best.pt")
    _model = best_model = YOLO(_best_weights, task="detect")

    def __init__(self):
        self.results = None

    def detect(self, image_paths):
        self.results = self._model(image_paths)
        return self.results

    def get_boxes(self):
        if not self.results:
            raise RuntimeError("Run detection first to get some results")
        boxes = map(lambda e: e.boxes, self.results)
        transformed = []
        for b in boxes:
            t = {}
            classes = np.unique(b.cls)
            for c in classes:
                t[c.item()] = []
            xywh = b.xywh
            for i in range(len(xywh)):
                t[b.cls[i].item()].append(xywh[i].tolist())
            transformed.append(t)
        return transformed
