import sys

from fdf.app import App
from fdf.model import Map
from fdf.parser import MapFormatError, parse_map


def main() -> None:
    if len(sys.argv) != 2:
        print("Использование: python main.py <файл.fdf>", file=sys.stderr)
        sys.exit(2)
        
    filepath = sys.argv[1]
    
    try:
        grid = parse_map(filepath)
        
        map_obj = Map(grid)
        
        app = App(map_obj)
        app.mainloop()
        
    except OSError as e:
        print(f"Ошибка доступа к файлу: {e}", file=sys.stderr)
        sys.exit(1)
    except MapFormatError as e:
        print(f"Ошибка формата: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()