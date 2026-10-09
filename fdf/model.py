from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    z: int
    color: str | None = None

class Map:
    def __init__(self, grid: list[list[tuple[int, str | None]]]):
        self._points: list[list[Point]] = []
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0
        
        for y, row in enumerate(grid):
            point_row = []
            for x, (z, color) in enumerate(row):
                point_row.append(Point(x=x, y=y, z=z, color=color))
            self._points.append(point_row)

    def __len__(self) -> int:
        "Возвращает общее количество точек на карте"
        return self.width * self.height

    def __iter__(self) -> Iterator[Point]:
        "Позволяет обходить все точки в цикле for"
        for row in self._points:
            yield from row

    def neighbors(self, p: Point) -> list[Point]:
        "Возвращает соседей точки: только справа и снизу"
        res = []
        if p.x + 1 < self.width:
            res.append(self._points[p.y][p.x + 1])
        if p.y + 1 < self.height:
            res.append(self._points[p.y + 1][p.x])
        return res