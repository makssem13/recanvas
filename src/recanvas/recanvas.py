from enum import Enum, auto
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk

class reObjT(Enum):
    OVAL = auto()
    RECT = auto()
    LINE = auto()
    POLY = auto()
    SKIP = auto()
    
class reObj:
    def __init__(self, t, coords, fill="#000000", outline="#000000", width=1):
        self.type = t
        self.coords = coords
        self.color = fill
        self.outline = outline
        self.width = width


class reCanvas:
    def __init__(self, root, width=100, height=100, bd=1, highlightthickness=1, bg="#000000", isdraw=True):
        self.objs = []
        if draw: self.canvas = tk.Canvas(root, width=width, height=height,\
                                bd=bd, highlightthickness=highlightthickness)
        self.x = width
        self.y = height
        self.root = root
        self.isdraw = draw
        self.basebuf = None
        self.buf = Image.new("RGB", (self.x, self.y), "white")
        self.screen = ImageTk.PhotoImage(self.buf, master=self.root)
        if self.isdraw: self.image_screen = self.canvas.create_image(0, 0, anchor="nw", image=self.screen)
        self.draw = None
        self.bg = bg
        
    def pack(self):
        if self.isdraw: self.canvas.pack()

    def winfo_height(self): return self.canvas.winfo_height() if self.isdraw else None

    def winfo_width(self): return self.canvas.winfo_width() if self.isdraw else None

    def create_rectangle(self, a, b, c, d, fill="#000000", outline="#000000", width=1):
        self.objs.append(reObj(reObjT.RECT, (a,b,c,d), fill=fill, outline=outline, width=width))
        return len(self.objs)-1
    
    def create_oval(self, a, b, c, d, fill="#000000", outline="#000000", width=1):
        self.objs.append(reObj(reObjT.OVAL, (a,b,c,d), fill=fill, outline=outline, width=width))
        return len(self.objs)-1
    
    def create_line(self, a, b, c, d, fill="#000000", outline="#000000", width=1):
        self.objs.append(reObj(reObjT.LINE, (a,b,c,d), fill=fill, outline=outline, width=width))
        return len(self.objs)-1

    def create_polygon(self, coords, fill="#000000", outline="#000000", width=1):
        self.objs.append(reObj(reObjT.POLY, coords, fill=fill, outline=outline, width=width))
        return len(self.objs)-1
    
    def move(self, objid, x, y):
        obj = self.objs[objid]
        x1, y1, x2, y2 = obj.coords
        obj.coords = (x1 + x, y1 + y, x2 + x, y2 + y)

    def delete(self, objid):
        self.objs[objid].type = reObjT.SKIP
       
    def clear(self):
        self.objs.clear()
       
    def coords(self, objid): return self.objs[objid].coords

    def focus_set(self):
        self.canvas.focus_set()

    def bind(self, key, func):
        self.canvas.bind(key, func)

    def get_buf(self):
        return self.buf
    
    def open_image_as_buf(self, path):
        self.basebuf = Image.open(path)
        self.draw = None
        return
    
    def update(self):
        if self.draw is None: self.draw = ImageDraw.Draw(self.buf)
        if self.basebuf is None: self.draw.rectangle((0,0,self.x,self.y), fill=self.bg)
        else:
            self.buf.paste(self.basebuf)
        for obj in self.objs:
            match obj.type:
                case reObjT.OVAL:
                    self.draw.ellipse(obj.coords, fill=obj.color, outline=obj.outline, width=obj.width)
                case reObjT.RECT:
                    self.draw.rectangle(obj.coords, fill=obj.color, outline=obj.outline, width=obj.width)
                case reObjT.LINE:
                    self.draw.line(obj.coords, fill=obj.color, width=obj.width)
                case reObjT.POLY:
                    self.draw.polygon(obj.coords, fill=obj.color, outline=obj.outline, width=obj.width)
        if self.isdraw:
            self.screen.paste(self.buf)
            self.canvas.itemconfig(self.image_screen, image=self.screen)
