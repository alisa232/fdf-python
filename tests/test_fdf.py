from pathlib import Path

import pytest

from fdf.model import Map, Point
from fdf.parser import MapFormatError, parse_map
from fdf.projection import Camera


# 1. Проверка разбора значений с цветами через parametrize 
@pytest.mark.parametrize("value_str, expected", [
    ("7", (7, None)),
    ("-3", (-3, None)),
    ("2,0xFF8800", (2, "#FF8800")),
    ("1,0xff", (1, "#0000FF")),
])
def test_parse_values(tmp_path: Path, value_str: str, expected: tuple[int, str | None]) -> None:
    file_path = tmp_path / "test.fdf"
    file_path.write_text(value_str, encoding="utf-8")
    grid = parse_map(str(file_path))
    assert grid[0][0] == expected

# 2. Ошибка формата: не число
def test_format_error_not_a_number(tmp_path: Path) -> None:
    file_path = tmp_path / "bad.fdf"
    file_path.write_text("1 2 x", encoding="utf-8")
    with pytest.raises(MapFormatError):
        parse_map(str(file_path))

# 3. Ошибка формата: пустой файл
def test_format_error_empty(tmp_path: Path) -> None:
    file_path = tmp_path / "empty.fdf"
    file_path.write_text("", encoding="utf-8")
    with pytest.raises(MapFormatError):
        parse_map(str(file_path))

# 4. Ошибка формата: строки разной длины
def test_format_error_unequal_rows(tmp_path: Path) -> None:
    file_path = tmp_path / "unequal.fdf"
    file_path.write_text("1 2 3\n1 2", encoding="utf-8")
    with pytest.raises(MapFormatError):
        parse_map(str(file_path))

# 4.5 Ошибка формата: не цвет
def test_format_error_bad_color(tmp_path: Path) -> None:
    file_path = tmp_path / "bad_color.fdf"
    file_path.write_text("1,0xGGGGGG", encoding="utf-8")
    with pytest.raises(MapFormatError):
        parse_map(str(file_path))

# 5. Разбор карты 5x5 и проверка центральной точки (высота 5)
def test_parse_elem_map(tmp_path: Path) -> None:
    content = (
        "0 0 0 0 0\n"
        "0 2 2 2 0\n"
        "0 2 5,0xFF0000 2 0\n"
        "0 2 2 2 0\n"
        "0 0 0 0 0\n"
    )
    file_path = tmp_path / "elem.fdf"
    file_path.write_text(content, encoding="utf-8")
    grid = parse_map(str(file_path))
    assert len(grid) == 5
    assert len(grid[0]) == 5
    assert grid[2][2] == (5, "#FF0000")

# 6. Проверка Модели: методы len, обход в цикле for и neighbors для угловой точки
def test_model_features() -> None:
    grid = [[(0, None), (1, None)], [(2, None), (3, None)]]
    m = Map(grid)
    assert len(m) == 4
    
    points = list(m)
    assert len(points) == 4
    
    # У точки (0, 0) есть сосед справа (1, 0) и снизу (0, 1)
    neighs = m.neighbors(Point(x=0, y=0, z=0))
    assert len(neighs) == 2

# 7. Проекция: точка (0, 0, 0) должна переходить в (0, 0)
def test_projection_zero() -> None:
    cam = Camera()
    cam.scale = 1.0
    cam.offset_x = 0.0
    cam.offset_y = 0.0
    x, y = cam.project(Point(x=0, y=0, z=0))
    assert x == 0.0
    assert y == 0.0

# 8. Проекция: точка с высотой (0, 0, 1) должна иметь отрицательную координату Y
def test_projection_height() -> None:
    cam = Camera()
    cam.scale = 1.0
    cam.offset_x = 0.0
    cam.offset_y = 0.0
    _, y = cam.project(Point(x=0, y=0, z=1))
    assert y < 0.0

# 9. Проекция: проверка центрирования и масштабирования (fit)
def test_projection_fit_bounds() -> None:
    cam = Camera()
    grid = [[(0, None), (1, None)], [(2, None), (3, None)]]
    m = Map(grid)
    width, height = 800, 600
    cam.fit(m, width, height)
    
    # Проверяем, что после подгонки ни одна точка не вылезла за границы экрана
    for p in m:
        x, y = cam.project(p)
        assert 0 <= x <= width
        assert 0 <= y <= height