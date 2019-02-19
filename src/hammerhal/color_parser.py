from typing import Tuple

from PIL import ImageColor

def __get_color(color) -> Tuple[int, ...]:
    _color = color
    if (isinstance(_color, int)):
        _color = "0x" + "{0:8x}".format(_color)
    if (isinstance(_color, str)):
        if (_color.startswith("0x")):
            s = _color
            # Color in ABGR
            _color = [int(s[i:i + 2], 16) for i in range(8, 0, -2)]
        else:
            _color = ImageColor.getcolor(_color, "RGBA")
    if (isinstance(_color, list)):
        _color = tuple(_color)

    return _color
