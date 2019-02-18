from enum import unique, auto
from functools import wraps
from typing import Callable, Any, List, Tuple

from PIL import Image, ImageDraw, ImageFont

from hammerhal.text_drawer import FontFinder, Obstacle
from hammerhal.text_drawer import PrintModes, TextAlignment, CapitalizationModes
from hammerhal import get_color
from logging import getLogger, Logger, DEBUG

from hammerhal.text_drawer.text_funcs import capitalize_first, capitalize, capitalize_smart

_logger = getLogger("text_drawer")
logger = _logger
import datetime

def log_time(func_name: str = None, logger: Logger = None, log_level: str = DEBUG):
    _func = None
    if (callable(func_name)):
        _func, func_name = func_name, _func
    if (logger is None):
        logger = _logger
    
    def wrapper(func: Callable):
        _func_name = func_name if (func_name is not None) else func.__name__
        
        @wraps(func)
        def wrapped(*args, **kwargs):
            _now = datetime.datetime.now()
            logger.log(log_level, "Calling %s", _func_name)
            result = func(*args, **kwargs)
            logger.log(log_level, "%s exit. Time spent: %ims", func_name, (datetime.datetime.now() - _now).total_seconds() * 1000)
            return result
        return wrapped
    
    if (_func is not None):
        return wrapper(_func)
    else:
        return wrapper

class TextDrawer:


    __drawer = None
    __font_finder = None

    __current_font_size = None
    __current_font_family = None
    __current_font_filepath = None
    __bold = None
    __italic = None

    __current_text_horizontal_alignment = None
    __current_text_vertical_alignment = None
    __current_text_capitalization = None
    __font_base = None

    character_width_scale  = None
    text_character_separator_scale = None
    text_vertical_space_scale = None
    text_paragraph_vertical_space = None
    text_space_scale = None

    color = None

    def __init__(self, im:Image.Image, font_family='Times New Roman', font_size=None, color=None, bold=None, italic=None, font_finder=None):
        if (font_finder):
            self.__font_finder = font_finder
        else:
            self.__font_finder = TextDrawer.get_default_text_finder()

        self.set_font(font_family=font_family, font_size=font_size, color=color, bold=bold, italic=italic)
        self.__drawer = ImageDraw.ImageDraw(im)

    @staticmethod
    def get_default_text_finder() -> FontFinder:
        if (not TextDrawer.__font_finder):
            TextDrawer.__font_finder = FontFinder()
        return TextDrawer.__font_finder

    def set_font(self, font_file=None, font_family=None, font_size=None, color=None, bold=None, italic=None, horizontal_alignment=None, vertical_alignment=None, character_width_scale=None, space_scale=None, vertical_space_scale=None, paragraph_vertical_space=None, character_separator_scale=None, capitalization=None):
        logger.debug("Requested font style change")
        self.__current_font_size = int(font_size or self.__current_font_size or 10)

        if (bold is not None):
            self.__bold = bold
        else:
            self.__bold = self.__bold or False

        if (italic is not None):
            self.__italic = italic
        else:
            self.__italic = self.__italic or False

        if ((not font_family is None) or (not bold is None) or (not italic is None)):
            _test_family = font_family or self.__current_font_family
            logger.debug("Changing current font file by family name ({font_family}{bold}{italic}) is not installed".format(font_family=_test_family, bold=", Bold" if self.__bold else '', italic=", Italic" if self.__italic else ''))
            _test_font = self.__font_finder.find_font_file_by_fontname(family_name=_test_family, bold=self.__bold, italic=self.__italic)
            if (_test_font):
                self.__current_font_family = _test_family
                self.__current_font_filepath = _test_font
            else:
                raise FileNotFoundError("Requested font ({font_family}{bold}{italic}) is not installed".format(font_family=_test_family, bold=", Bold" if self.__bold else '', italic=", Italic" if self.__italic else ''))

        elif (not font_file is None):
            logger.debug("Changing current font file (direct): '{font_file}'".format(font_file=font_file))
            _test_font = self.__font_finder.find_font_file_by_filename(font_file)
            if (_test_font):
                self.__current_font_family = None
                self.__current_font_filepath = _test_font
            else:
                raise FileNotFoundError("Requested font ('{font_file}') is not installed".format(font_file=font_file))

        else:
            logger.debug("Font should not be changed: '{font_file}'".format(font_file=self.__current_font_filepath))

        self.__font_base = ImageFont.truetype(font=self.__current_font_filepath, size=self.__current_font_size, encoding='unic')

        self.__current_text_vertical_alignment = TextAlignment.find_value(vertical_alignment) or self.__current_text_vertical_alignment or TextAlignment.Top
        self.__current_text_horizontal_alignment = TextAlignment.find_value(horizontal_alignment) or self.__current_text_horizontal_alignment or TextAlignment.Left
        self.__current_text_capitalization = CapitalizationModes.find_value(capitalization) or self.__current_text_capitalization or CapitalizationModes.Normal

        if (not space_scale is None):
            self.text_space_scale = space_scale
        else:
            self.text_space_scale = self.text_space_scale or 1.0

        if (not vertical_space_scale is None):
            self.text_vertical_space_scale = vertical_space_scale
        else:
            self.text_vertical_space_scale = self.text_vertical_space_scale or 0.0

        if (not paragraph_vertical_space is None):
            self.text_paragraph_vertical_space = paragraph_vertical_space
        else:
            self.text_paragraph_vertical_space = self.text_paragraph_vertical_space or 0

        if (not character_separator_scale is None):
            self.text_character_separator_scale = character_separator_scale
        else:
            self.text_character_separator_scale = self.text_character_separator_scale or 0.0

        if (not character_width_scale is None):
            self.character_width_scale = character_width_scale
        else:
            self.character_width_scale = self.character_width_scale or 1.0

        if (color or not self.color):
            self.color = get_color(color or self.color or 'white')

        logger.debug("Current font: {0}".format(self.get_font()))

    def get_font(self):
        result_dict = \
        {
            'font_file': self.__current_font_filepath,
            'font_family': self.__current_font_family,
            'font_size': self.__current_font_size,
            'color': self.color,
            'bold': self.__bold,
            'italic': self.__italic,
            'horizontal_alignment': self.__current_text_horizontal_alignment,
            'vertical_alignment': self.__current_text_vertical_alignment,
            'character_width_scale': self.character_width_scale,
            'space_scale': self.text_space_scale,
            'vertical_space_scale': self.text_paragraph_vertical_space,
            'paragraph_vertical_space': self.text_paragraph_vertical_space,
            'character_separator_scale': self.text_character_separator_scale,
            'capitalization': self.__current_text_capitalization,
        }

        return result_dict

    @log_time("Line print")
    def print_line(self, position, text:str):
        logger.debug("Printing text line: '{text}'".format(text=text))
        self.__print(position, text, print_mode=PrintModes.NormalPrint)

    @log_time("Text region print")
    def print_in_region(self, region, text:str, offset_borders:bool=True, obstacles=None) -> Tuple[int, int]:
        logger.debug("Printing text region: '{text}'".format(text=text))
        result = self.__print_in_region(region, text, offset_borders, real_print=True, obstacles=obstacles)
        return result

    @log_time("Text region size")
    def get_text_size(self, region, text:str, offset_borders:bool=True, obstacles: List[Obstacle]=None) -> Tuple[int, int]:
        logger.debug("Requested region text size: '{text}'".format(text=text))
        result = self.__print_in_region(region, text, offset_borders, real_print=False, obstacles=obstacles)
        return result

    def __print_in_region(self, region, text:str, offset_borders, real_print, obstacles: List[Obstacle]) -> Tuple[int, int]:
        if (offset_borders):
            x, y, w, h = region
        else:
            x, y, x2, y2 = region
            w = x2 - x
            h = y2 - y

        max_width = 0
        space_width, _ = self.__print(None, ' ', print_mode=PrintModes.GetTextSize)
        # _, line_height = self.__print(None, 'LINE HEIGHT (gyq,)', print_mode=PrintModes.GetTextSize)
        _, line_height = self.__print(None, 'LINE HEIGHT', print_mode=PrintModes.GetTextSize)

        paragraphs = []
        for paragraph_text in text.split('\n'):
            _horizontal_alignment = self.__current_text_horizontal_alignment
            words = paragraph_text.split()
            paragraph_obj = { "lines": [], "horizontal_alignment": _horizontal_alignment }
            i = 0
            while (i < len (words)):
                word = words[i]
                if (word.startswith('$$')):
                    if (False):
                        pass
                    elif (word == '$$HA_L'):
                        paragraph_obj['horizontal_alignment'] = TextAlignment.Left
                    elif (word == '$$HA_C'):
                        paragraph_obj['horizontal_alignment'] = TextAlignment.Center
                    elif (word == '$$HA_R'):
                        paragraph_obj['horizontal_alignment'] = TextAlignment.Right
                    elif (word == '$$HA_J'):
                        paragraph_obj['horizontal_alignment'] = TextAlignment.Justify
                    else:
                        raise KeyError("Unsupported operand: {word}".format(word=word))

                    del words[i]

                else:
                    i += 1

            _lines = self.__print(None, ' '.join(words), print_mode=PrintModes.SplitLines, line_width=w, obstacles=obstacles)
            logger.debug("Splitting paragraph to lines: '{0}' -> '{1}'".format(paragraph_text, _lines))
            for line_text, line_width in _lines:
                paragraph_obj['lines'].append( { 'words': line_text.split(), 'width': line_width } )
                if (max_width < line_width):
                    max_width = line_width

            paragraphs.append(paragraph_obj)

        num_lines = sum(len(paragraph_obj['lines']) for paragraph_obj in paragraphs)
        total_height = int(num_lines * (1 + self.text_vertical_space_scale) * line_height + self.text_paragraph_vertical_space * (len(paragraphs) - 1))

        if (real_print):

            if (obstacles):
                _current_obstacle = 0

            if (self.__current_text_vertical_alignment == TextAlignment.Bottom):
                _y = y + h - total_height

            elif (self.__current_text_vertical_alignment == TextAlignment.Center):
                _y = y + (h - total_height) // 2
            else:
                _y = y

            for paragraph_obj in paragraphs:
                paragraph_lines = paragraph_obj['lines']
                for i in range(len(paragraph_lines)):
                    line = paragraph_lines[i]
                    last_line = (i + 1 == len(paragraph_lines))

                    _local_w = w
                    _obstacle = None
                    if (obstacles):
                        _obstacle = obstacles[_current_obstacle]
                        while (y >= obstacles[_current_obstacle].y2):
                            _current_obstacle += 1
                            if (_current_obstacle >= len(obstacles)):
                                obstacles = None
                                _obstacle = None
                                break
                            _obstacle = obstacles[_current_obstacle]

                    if (_obstacle):
                        if ((_y <= _obstacle.y1 <= y + h) or (_obstacle.y1 <= _y <= _obstacle.y2)):
                            _local_w = _obstacle.x

                    new_space_width = space_width
                    if (paragraph_obj['horizontal_alignment'] == TextAlignment.Right):
                        _x = x + _local_w - line['width']
                    elif (paragraph_obj['horizontal_alignment'] == TextAlignment.Center):
                        _x = x + (_local_w - line['width']) // 2
                    elif (paragraph_obj['horizontal_alignment'] == TextAlignment.Justify and not last_line and len(line['words']) > 0):
                        _x = x
                        num_spaces = len(line['words']) - 1
                        if (num_spaces > 0):
                            new_space_width = space_width + (_local_w - line['width']) / num_spaces
                    else:
                        _x = x

                    self.__print((_x, _y), ' '.join(line['words']), print_mode=PrintModes.NormalPrint, restricted_space_width=new_space_width)
                    _y += (1 + self.text_vertical_space_scale) * self.__current_font_size
                _y += self.text_paragraph_vertical_space
        
        assert max_width <= w, "Max width exceeded"
        return max_width, total_height


    def __print(self, position, text: str, print_mode, restricted_space_width=None, debug_console_print: bool = False, **kwargs):
        x, y = position or (0, 0)
        max_height = 0

        _text = text
        if (self.__current_text_capitalization == CapitalizationModes.UpperCase):
            _text = _text.upper()
        elif (self.__current_text_capitalization == CapitalizationModes.LowerCase):
            _text = _text.lower()
        elif (self.__current_text_capitalization == CapitalizationModes.Capitalize):
            _text = capitalize(_text)
        elif (self.__current_text_capitalization == CapitalizationModes.CapitalizeSmart):
            _text = capitalize_smart(_text)
        elif (self.__current_text_capitalization == CapitalizationModes.CapitalizeFirst):
            _text = capitalize_first(_text)

        if (print_mode == PrintModes.SplitLines):
            _line_splits: List[Tuple[str, int]] = list()
            _line_start = 0
            _line_start_x = 0
            _line_width = kwargs.get('line_width', None)
            x = 0
            _word_start = 0
            _word_start_x = 0
            _last_word_end = 0
            _last_word_end_x = 0
            if (_line_width is None):
                raise ValueError("'line_width' argument is required for the SplitLines mode")

            _obstacles: List[Obstacle] = kwargs.get('obstacles', None)
            _current_obstacle = 0

        original_bold = self.__bold
        original_italic = self.__italic
        _continue = False

        if (self.__current_text_capitalization == CapitalizationModes.SmallCaps):
            # _, _new_size = self._drawer.textsize(_char, font=_font)
            _new_size = int(self.__current_font_size * 0.75)
            _char = 'ixz'
            _char = _char.upper()

            _font = self.__font_base
            _small_caps_font = ImageFont.truetype(font=self.__current_font_filepath, size=_new_size, encoding='unic')
            _, _y1 = self.__drawer.textsize(_char, font=_small_caps_font)
            _, _y2 = self.__drawer.textsize(_char, font=_font)
            _small_caps_dy = _y2 - _y1
        
        _len = len(text)
        for i in range(_len):
            if (_continue):
                _continue = False

                if (self.__current_text_capitalization == CapitalizationModes.SmallCaps):
                    # _, _new_size = self._drawer.textsize(_char, font=_font)
                    _new_size = int(self.__current_font_size * 0.75)
                    _char = 'ixz'
                    _char = _char.upper()

                    _font = self.__font_base
                    _small_caps_font = ImageFont.truetype(font=self.__current_font_filepath, size=_new_size, encoding='unic')
                    _, _y1 = self.__drawer.textsize(_char, font=_font)
                    _, _y2 = self.__drawer.textsize(_char, font=_small_caps_font)
                    _small_caps_dy = _y2 - _y1

                continue
            if (i + 2 <= _len):
                if (_text[i:i + 2] == '__'):
                    logger.debug("Change font style to {}italic".format('non-' * self.__italic))
                    self.set_font(italic=not self.__italic)
                    _continue = True
                    continue
                if (_text[i:i + 2] == '**'):
                    logger.debug("Change font style to {}bold".format('non-' * self.__bold))
                    self.set_font(bold=not self.__bold)
                    _continue = True
                    continue

            _char = _text[i];
            _x = int(x);
            _y = int(y);
            _font = self.__font_base

            if (self.__current_text_capitalization == CapitalizationModes.SmallCaps and _char != _char.upper()):
                _char = _char.upper()
                _y += _small_caps_dy
                _font = _small_caps_font
            w, h = self.__drawer.textsize(_char, font=_font)
            if (print_mode == PrintModes.NormalPrint):
                if (debug_console_print):
                    print(text[i], end='')
                self.__drawer.text((_x, _y), _char, self.color, font=_font)
            if (_char == ' ' or i == _len - 1):
                _space_width = restricted_space_width if restricted_space_width else w * self.text_space_scale
                
                if (print_mode == PrintModes.SplitLines):

                    _local_line_width = _line_width
                    _obstacle = None
                    if (_obstacles):
                        _obstacle = _obstacles[_current_obstacle]
                        while (y >= _obstacles[_current_obstacle].y2):
                            _current_obstacle += 1
                            if (_current_obstacle >= len(_obstacles)):
                                _obstacles = None
                                _obstacle = None
                                break
                            _obstacle = _obstacles[_current_obstacle]

                    if (_obstacle):
                        if ((y <= _obstacle.y1 <= y + h) or (_obstacle.y1 <= y <= _obstacle.y2)):
                            _local_line_width = _obstacle.x

                    _local_line_width -= _space_width
                    
                    if ((x - _line_start_x) > _local_line_width):
                        _current_line_width = _last_word_end_x - _line_start_x
                        logger.debug("Line shift required after '%s'", text[_line_start:_last_word_end])
                        assert _current_line_width <= _local_line_width, "Line width exceeded"
                        _line_splits.append((text[_line_start:_last_word_end], _current_line_width))
                        _line_start = _word_start
                        _line_start_x = _word_start_x
                        y += max_height
                        max_height = 0
                    elif (i > 1 and _text[i - 1] != ' '):
                        _last_word_end = i
                        _last_word_end_x = x
                
                x += _space_width
                _word_start = i + 1
                _word_start_x = x

            else:
                x += w + self.text_character_separator_scale * self.__current_font_size
            if (max_height < h):
                max_height = h

        initial_x, _ = position or (0, 0)
        if (debug_console_print):
            print('', end='\n')
        self.set_font(bold=original_bold, italic=original_italic)

        if (print_mode == PrintModes.SplitLines):
            _current_line_width = x - _line_start_x
            assert _current_line_width <= _line_width, "Last line width exceeded"
            _line_splits.append((text[_line_start:], _current_line_width))
            return _line_splits
        else:
            return (x - initial_x, max_height)
