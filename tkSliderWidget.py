from tkinter import *
from tkinter.ttk import *

from typing import TypedDict, List, Union, Callable


class Bar(TypedDict):
    Ids: List[int]
    Pos: float
    Value: float
    Pos0: float

class Slider(Frame):
    LINE_COLOR = "#476b6b"
    LINE_WIDTH = 3
    BAR_COLOR_INNER = "#5c8a8a"
    BAR_COLOR_OUTTER = "#c2d6d6"
    BAR_RADIUS = 10
    BAR_RADIUS_INNER = BAR_RADIUS - 5
    DIGIT_PRECISION = ".1f"  # for showing in the canvas
    TEXT_PRECISION = ".0f"

    # relative step size in 0 to 1, set to 0 for no step size restiction
    STEP_SIZE:float = 0.0

    def __init__(
        self,
        master,
        width=400,
        height=80,
        from_ = 0,
        to = 10,
        min_val=0,
        max_val=1,
        init_lis=None,
        show_value=True,
        removable=False,
        addable=False,
    ):
        Frame.__init__(self, master, height=height, width=width)
        self.master = master
        if init_lis == None:
            init_lis = [min_val]
        self.init_lis = init_lis
        self.from_ = from_
        self.to = to
        self.max_val = max_val
        self.min_val = min_val
        self.show_value = show_value
        self.H = height
        self.W = width
        self.canv_H = self.H
        self.canv_W = self.W
        if not show_value:
            self.slider_y = self.canv_H / 2  # y pos of the slider
        else:
            self.slider_y = self.canv_H / 5
        self.slider_x = Slider.BAR_RADIUS  # x pos of the slider (left side)

        self._val_change_callback = lambda lis: None

        self.bars: List[Bar] = []
        self.selected_idx = None  # current selection bar index

        for value in self.init_lis:
            pos = (value - min_val) / (max_val - min_val)
            pos0 = value
            ids = []
            bar: Bar = {"Pos": pos, "Ids": ids, "Value": value, "Pos0": pos0}
            self.bars.append(bar)

        self.canv = Canvas(self, height=self.canv_W, width=self.canv_W, relief=RAISED)
        self.canv.pack()
        self.canv.bind("<Motion>", self._mouseMotion)
        self.canv.bind("<B1-Motion>", self._moveBar)
        if removable:
            self.canv.bind("<3>", self._removeBar)
        if addable:
            self.canv.bind("<ButtonRelease-1>", self._addBar)
        self.__addTrack(
            self.slider_x, self.slider_y, self.canv_W - self.slider_x, self.slider_y
        )
        for bar in self.bars:
            bar["Ids"] = self.__addBar(bar["Pos"], bar["Pos0"])

    def getValues(self) -> List[float]:
        values = [bar["Value"] for bar in self.bars]
        return sorted(values)
    
    def setValueChageCallback(self, callback: Callable[[List[float]], None]):
        self._val_change_callback = callback

    def _mouseMotion(self, event):
        x = event.x
        y = event.y
        selection = self.__checkSelection(x, y)
        if selection[0]:
            self.canv.config(cursor="hand2")
            self.selected_idx = selection[1]
        else:
            self.canv.config(cursor="")
            self.selected_idx = None

    def _moveBar(self, event):
        x = event.x
        y = event.y
        if self.selected_idx == None:
            return False
        pos = self.__calcPos(x)
        idx = self.selected_idx
        pos0 = self.bars[idx]["Pos0"]
        if self.STEP_SIZE > 0:
            curr_pos = self.bars[idx]["Pos"]
            if abs(curr_pos - pos) < self.STEP_SIZE:
                return
        self.__moveBar(idx, pos, pos0)

    def _removeBar(self, event):
        x = event.x
        y = event.y
        if self.selected_idx == None:
            return False
        idx = self.selected_idx
        ids = self.bars[idx]["Ids"]
        for id in ids:
            self.canv.delete(id)
        self.bars.pop(idx)

    def _addBar(self, event):
        x = event.x
        y = event.y

        if self.selected_idx == None:
            pos = self.__calcPos(x)
            ids = []
            pos0 = float
            bar = {
                "Pos": pos,
                "Ids": ids,
                "Value": self.__calcPos(x) * (self.max_val - self.min_val),
                "Pos0": pos0
                + self.min_val,
            }
            self.bars.append(bar)

            for i in self.bars:
                ids = i["Ids"]
                for id in ids:
                    self.canv.delete(id)

            for bar in self.bars:
                bar["Ids"] = self.__addBar(bar["Pos"], bar["Pos0"])


    def __addTrack(self, startx, starty, endx, endy):
        id1 = self.canv.create_line(
            startx, starty, endx, endy, fill=Slider.LINE_COLOR, width=Slider.LINE_WIDTH
        )
        return id

    def __addBar(self, pos, pos0):
        """@ pos: position of the bar, ranged from (0,1)"""
        if pos < 0 or pos > 1:
            raise Exception("Pos error - Pos: " + str(pos))
        R = Slider.BAR_RADIUS
        r = Slider.BAR_RADIUS_INNER
        L = self.canv_W - 2 * self.slider_x
        y = self.slider_y
        x = self.slider_x + pos * L
        id_outer = self.canv.create_oval(
            x - R,
            y - R,
            x + R,
            y + R,
            fill=Slider.BAR_COLOR_OUTTER,
            width=2,
            outline="",
        )
        id_inner = self.canv.create_oval(
            x - r, y - r, x + r, y + r, fill=Slider.BAR_COLOR_INNER, outline=""
        )
        if self.show_value:
            for id in range(len(self.bars)):
                y_value = y + Slider.BAR_RADIUS + 8
                value = pos0
                id_value = self.canv.create_text(x, y_value, text=format(value, Slider.TEXT_PRECISION)
                )
                return [id_outer, id_inner, id_value]
        else:
            return [id_outer, id_inner]


    def __moveBar(self, idx, pos, pos0):
        ids = self.bars[idx]["Ids"]
        for id in ids:
            self.canv.delete(id)
        self.bars[idx]["Ids"] = self.__addBar(pos, pos0)
        self.bars[idx]["Pos"] = pos
        self.bars[idx]["Value"] = pos * (self.max_val - self.min_val) + self.min_val
        self._val_change_callback(self.getValues())

    def __calcPos(self, x):
        """calculate position from x coordinate"""
        pos = (x - self.slider_x) / (self.canv_W - 2 * self.slider_x)
        if pos < 0:
            return 0
        elif pos > 1:
            return 1
        else:
            return pos

    def __calcPos0(self, idx):
        """calculate position from x coordinate"""
        pos = (x - self.slider_x) / (self.canv_W - 2 * self.slider_x)
        if pos < 0:
            return 0
        elif pos > 1:
            return 1
        else:
            return pos0


    def __checkSelection(self, x, y):
        """
        To check if the position is inside the bounding rectangle of a Bar
        Return [True, bar_index] or [False, None]
        """
        for idx in range(len(self.bars)):
            id = self.bars[idx]["Ids"][0]
            bbox = self.canv.bbox(id)
            if bbox[0] < x and bbox[2] > x and bbox[1] < y and bbox[3] > y:
                return [True, idx]
        return [False, None]

import tkinter as tk
from tkSliderWidget import Slider

root = tk.Tk()
life_sat=tk.StringVar()
life_sat = life_sat.set("")

slider = Slider(root, width = 500, height = 500, min_val = 0, max_val = 10, init_lis = [1,2,3,4,5,6,7,8,9], show_value = TRUE)
name_label = tk.Label(root, text = 'My current life satisfaction is: (out of 10)', font=('calibre',10, 'bold'))
entry = tk.Entry(root, textvariable = life_sat, font=('calibre',10,'normal'))
l3 = Label(root, text = "Life Satisfaction Scale")
b1 = Button(root, text ="Done")

name_label.pack()
entry.pack()
slider.pack()
l3.pack(anchor=CENTER)
b1.pack(anchor=CENTER)
# optionally add a callback on value change
slider.setValueChageCallback(lambda vals: print(vals))

root.title("Life Satisfaction Scale")
root.mainloop()

print(slider.getValues())
