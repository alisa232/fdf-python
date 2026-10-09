import math

from fdf.model import Map, Point


class Camera:
    def __init__(self) -> None:
        self.angle: float = math.radians(30)
        self.z_scale: float = 1.0
        self.scale: float = 1.0
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0

    def project(self, p: Point) -> tuple[float, float]:
        "Проецирует 3D-точку на 2D-плоскость окна"
        x_prime = (p.x - p.y) * math.cos(self.angle)
        y_prime = (p.x + p.y) * math.sin(self.angle) - (p.z * self.z_scale)
        
        X = x_prime * self.scale + self.offset_x
        Y = y_prime * self.scale + self.offset_y
        return X, Y

    def fit(self, map_obj: Map, width: int, height: int) -> None:
        "Подбирает масштаб и сдвиг, чтобы карта поместилась в окно"
        if len(map_obj) == 0:
            return

        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for p in map_obj:
            px, py = self.project(p)
            min_x = min(min_x, px)
            max_x = max(max_x, px)
            min_y = min(min_y, py)
            max_y = max(max_y, py)

        map_width = max_x - min_x
        map_height = max_y - min_y

        if map_width == 0 or map_height == 0:
            self.scale = 1.0
        else:
            self.scale = min(width / map_width, height / map_height) * 0.9

        center_x = min_x * self.scale + (map_width * self.scale) / 2
        center_y = min_y * self.scale + (map_height * self.scale) / 2

        self.offset_x = (width / 2) - center_x
        self.offset_y = (height / 2) - center_y