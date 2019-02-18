from typing import List, Tuple

from PIL import ImageFont
from PIL.ImageDraw import ImageDraw
from typing_tools import DictStruct

from hammerhal.text_drawer import CapitalizationModes, PrintModes, TextAlignment
from hammerhal.text_drawer.text_funcs import capitalize_first

class Obstacle(DictStruct):
    x: int
    y1: int
    y2: int

class ParagraphObject(DictStruct):
    lines: List[str] = []
    horizontal_alignment: TextAlignment

class Printer:
    drawer: ImageDraw
    
    _text: str
    _lines: List[Tuple[str, int]]
    
    def print_simple(self, text: str):
        pass
    def print_split(self, text: str):
        pass
    
    def _print_text(self, position: Tuple[int, int], c: str):
        self.drawer.text(position, c, self.color, font=self.font)
    
    def _get_text_size(self, c: str):
        w, h = self.drawer.textsize(c, font=self.font)
        return w, h
