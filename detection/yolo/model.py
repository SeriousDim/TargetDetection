from abc import abstractmethod


class DetectionModel:
    def __init__(self):
        self.results = None

    @abstractmethod
    def detect(self, image_paths):
        pass

    @abstractmethod
    def get_boxes(self):
        pass
