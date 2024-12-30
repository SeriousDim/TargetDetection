from app.models.dto.hit import Hit
from app.models.dto.target import Target
from app.models.geometry.point import GeometricalPoint


def target_label_to_name(label):
    return {0.0: "4", 1.0: "6", 2.0: "6в"}[label]


def boxes_to_targets(class_lists):
    targets = []
    current_id = 0

    for label in class_lists.keys():
        boxes = class_lists[label]
        for box in boxes:
            targets.append(
                Target(
                    id=current_id,
                    name=target_label_to_name(label),
                    center=GeometricalPoint(x=box[0], y=box[1]),
                    width=box[2],
                    height=box[3],
                )
            )
            current_id += 1
    return targets


def boxes_to_hits(class_lists):
    hits = []
    current_id = 0

    if not class_lists.keys():
        return hits
    boxes = class_lists[0]

    for box in boxes:
        hits.append(
            Hit(
                id=current_id,
                center=GeometricalPoint(x=box[0], y=box[1]),
                width=box[2],
                height=box[3],
            )
        )
        current_id += 1
    return hits
