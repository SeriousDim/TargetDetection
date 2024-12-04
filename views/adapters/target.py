from detection.dto.hit import Hit
from detection.dto.target import Target
from geometry.point import GeometricalPoint


def get_boxes_with_labels(class_lists, class_label):
    try:
        coords = class_lists[class_label]
    except KeyError:
        return []
    boxes = []

    for i in range(len(coords)):
        c = coords[i]
        boxes.append(Target(
            id=i,
            center=GeometricalPoint(x=c[0], y=c[1]),
            width=c[2],
            height=c[3]
        ))

    return boxes


# ! Изменил
def model_boxes_to_targets(class_lists):
    targets = []
    target_coords = class_lists.get(0.0, [])

    for i, c in enumerate(target_coords):
        targets.append(
            Target(
                id=i,
                center=GeometricalPoint(x=c[0], y=c[1]),
                width=c[2],
                height=c[3],
            )
        )
    return targets


def model_boxes_to_hits(class_lists):
    try:
        coords = class_lists[0]
    except KeyError:
        return []
    hits = []

    for i in range(len(coords)):
        c = coords[i]
        hits.append(Hit(
            id=i,
            center=GeometricalPoint(x=c[0], y=c[1]),
            width=c[2],
            height=c[3]
        ))

    return hits
