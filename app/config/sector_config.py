from app.models.geometry.point import GeometricalPoint
from app.models.sectors.angle_sector import AngleSector
from app.models.sectors.circle_sector import CircleSector
from app.models.sectors.off_target_sector import (
    BelowTargetSector,
    OutOfBoundsSector,
)


class SectorConfig:
    angle_sectors = AngleSector.create_list(
        [
            [[-0.23, 0.5], [-0.5, 0.18]],
            [[-0.5, 0.18], [-0.5, -0.14]],
            [[-0.5, -0.14], [-0.23, -0.5]],
            [[-0.23, -0.5], [0.23, -0.5]],
            [[0.23, -0.5], [0.5, -0.14]],
            [[0.5, -0.14], [0.5, 0.18]],
            [[0.5, 0.18], [0.23, 0.5]],
            [[0.23, 0.5], [-0.23, 0.5]],
        ],
        ["2", "3", "4", "5", "6", "7", "8", "9"],
    )
    center_sector = CircleSector(
        name="1", center=GeometricalPoint(x=0.0, y=0.0), radius=0.1
    )

    # Сектор для попаданий ниже мишени
    below_target_sector = BelowTargetSector(name="10")

    # Сектор для попаданий вне мишени (сверху, слева, справа)
    out_of_bounds_sector = OutOfBoundsSector(name="0")

    line_width = 3
