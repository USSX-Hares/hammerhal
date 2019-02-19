import inspect
from enum import Enum, auto
from typing import Optional

class ExtendedEnum(Enum):
    @classmethod
    def find_value(cls, key) -> Optional['ExtendedEnum']:
        if (isinstance(key, str)):
            _members = inspect.getmembers(cls)
            for _member in _members:
                if (_member[0] == key):
                    # print("{0} is {1}!".format(*_member))
                    return _member[1]

            # print("{0} not found".format(key))
            return None

        else:
            # print("{0} is not a string; returning it")
            return key

class CapitalizationModes(ExtendedEnum):
    Normal = auto()
    UpperCase = auto()
    AllCaps = auto()
    LowerCase = auto()
    NoCaps = auto()
    Capitalize = auto()
    CapitalizeFirst = auto()
    CapitalizeSmart = auto()
    SmallCaps = auto()

class TextAlignment(ExtendedEnum):
    Left = 1
    Top = 1
    Center = 2
    Right = 3
    Bottom = 3
    Justify = 4

class PrintModes(ExtendedEnum):
    NormalPrint = auto()
    GetTextSize = auto()
    SplitLines = auto()
