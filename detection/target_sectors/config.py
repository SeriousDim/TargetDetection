from geometry.point import GeometricalPoint
from sectors.angle_sector import AngleSector
from sectors.circle_sector import CircleSector


class SectorConfig:
    angle_sectors = AngleSector.create_list([
        [[-0.23, 0.5], [-0.5, 0.18]],
        [[-0.5, 0.18], [-0.5, -0.14]],
        [[-0.5, -0.14], [-0.23, -0.5]],
        [[-0.23, -0.5], [0.23, -0.5]],
        [[0.23, -0.5], [0.5, -0.14]],
        [[0.5, -0.14], [0.5, 0.18]],
        [[0.5, 0.18], [0.23, 0.5]],
        [[0.23, 0.5], [-0.23, 0.5]],
    ], ['2', '3', '4', '5', '6', '7', '8', '9',])
    center_sector = CircleSector(
        name='1',
        center=GeometricalPoint(x=0.0, y=0.0),
        radius=0.1
    )
    line_width = 3
