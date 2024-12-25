from abc import abstractmethod

import numpy as np


class DetectionModel:
    def __init__(self):
        self.results = None

    @abstractmethod
    def detect(self, image_paths):
        pass

    def get_boxes(self):
        if not self.results:
            raise RuntimeError("Run detection first to get some results")
        boxes = map(lambda e: e.boxes, self.results)
        transformed = {}
        for b in boxes:
            classes = np.unique(b.cls)
            for c in classes:
                if c.item() not in transformed.keys():
                    transformed[c.item()] = []
            xywh = b.xywh
            for i in range(len(xywh)):
                transformed[b.cls[i].item()].append(xywh[i].tolist())
        return transformed
