from app.models.geometry.geometry import Geometry
from app.models.geometry.point import GeometricalPoint
from app.services.hit_service import calculate_iou


def calculate_iou_for_result(predicted, truth):
    return calculate_iou(
        Geometry(
            center=GeometricalPoint(x=truth[0], y=truth[1]),
            width=truth[2],
            height=truth[3]
        ),
        Geometry(
            center=GeometricalPoint(x=predicted[0], y=predicted[1]),
            width=predicted[2],
            height=predicted[3]
        )
    )
