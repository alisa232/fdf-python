class FdfError(Exception):
    "Базовая ошибка проекта"

class MapFormatError(FdfError):
    "Ошибка формата файла карты"
    def __init__(self, message: str):
        super().__init__(message)

def parse_map(filepath: str) -> list[list[tuple[int, str | None]]]:
    grid: list[list[tuple[int, str | None]]] = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for row_idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            
            row_data: list[tuple[int, str | None]] = []
            values = line.split()
            
            for col_idx, val in enumerate(values, start=1):
                parts = val.split(',')
                height_str = parts[0]
                color_str = None
                
                try:
                    height = int(height_str)
                except ValueError:
                    raise MapFormatError(f"строка {row_idx}, колонка {col_idx}: '{height_str}' — не целое число")
                    
                if len(parts) > 1:
                    raw_color = parts[1].strip()
                    if not raw_color.lower().startswith('0x'):
                        raise MapFormatError(f"строка {row_idx}, колонка {col_idx}: '{raw_color}' — неверный формат цвета")
                    hex_part = raw_color[2:]
                    try:
                        int(hex_part, 16)
                        color_str = f"#{hex_part.upper().zfill(6)}"
                    except ValueError:
                        raise MapFormatError(f"строка {row_idx}, колонка {col_idx}: '{raw_color}' — некорректный цвет")
                
                row_data.append((height, color_str))
            
            grid.append(row_data)
            
    if not grid:
        raise MapFormatError("строка 1, колонка 1: пустой файл")
        
    expected_width = len(grid[0])
    for row_idx, row in enumerate(grid, start=1):
        if len(row) != expected_width:
            raise MapFormatError(f"строка {row_idx}, колонка 1: длина строки не совпадает с первой")
            
    return grid