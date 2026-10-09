import tkinter as tk

from fdf.model import Map
from fdf.projection import Camera


class App(tk.Tk):
    def __init__(self, map_obj: Map):
        super().__init__()
        self.title("FdF — каркасная 3D-модель")
        self.map_obj = map_obj
        self.camera = Camera()
        
        self.width = 1000
        self.height = 700
        self.geometry(f"{self.width}x{self.height}")
        
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="#1E1E2E")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.bind("<Escape>", lambda e: self.destroy())
        
        self.bind("<Configure>", self.on_resize)
        
        self.draw()

    def on_resize(self, event: tk.Event) -> None:
        "Обработчик изменения размера окна"
       
        if event.widget == self and (event.width != self.width or event.height != self.height):
            self.width = event.width
            self.height = event.height
            self.draw()

    def draw(self) -> None:
        "Отрисовка каркаса"
        self.canvas.delete("all")
        
        self.camera.fit(self.map_obj, self.width, self.height)
        
        for p in self.map_obj:
            x1, y1 = self.camera.project(p)
            
            color = p.color if p.color else "#4A90E2"
            
            for neighbor in self.map_obj.neighbors(p):
                x2, y2 = self.camera.project(neighbor)
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)