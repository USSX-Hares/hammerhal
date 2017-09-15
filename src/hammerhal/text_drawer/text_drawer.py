from PIL import Image, ImageDraw, ImageFont
from hammerhal.text_drawer import FontFinder

class TextDrawer:

    class CapitalizationModes:
        Normal = 1
        UpperCase = 2
        AllCaps = 2
        LowerCase = 3
        NoCaps = 3
        Capitalize = 4
        SmallCaps = 5

    class TextAlignment:
        Left = 1
        Top = 1
        Center = 2
        Right = 3
        Bottom = 3
        Justify = 4

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

    def __init__(self, im:Image.Image, font_family=None, font_size=None, color=None, bold=None, italic=None, font_finder=None):
        if (font_finder):
            self.__font_finder = font_finder
        else:
            if (not TextDrawer.__font_finder):
                TextDrawer.__font_finder = FontFinder()
            self.__font_finder = TextDrawer.__font_finder

        self.set_font(font_family=font_family, font_size=font_size, color=color, bold=bold, italic=italic)
        self.__drawer = ImageDraw.ImageDraw(im)

    def set_font_direct(self, font_filename):
        self.__current_font_filepath = self.__font_finder.find_font_file_by_filename(font_filename) or self.__current_font_filepath
        self.__font_base = ImageFont.truetype(font=self.__current_font_filepath, size=self.__current_font_size, encoding='unic')

    def set_font(self, font_family=None, font_size=None, color=None, bold=None, italic=None, horizontal_alignment=None, vertical_alignment=None, character_width_scale=None, space_scale=None, vertical_space_scale=None, paragraph_vertical_space=None, character_separator_scale=None, capitalization=None):
        self.__current_font_size = font_size or self.__current_font_size or 10
        self.__current_font_family = font_family or self.__current_font_family or 'Times New Roman'

        if (not bold is None):
            self.__bold = bold
        else:
            self.__bold = self.__bold or False

        if (not italic is None):
            self.__italic = italic or self.__italic or False
        else:
            self.__italic = self.__italic or False

        if not (font_family is None and bold is None and italic is None):
            self.__current_font_filepath = self.__font_finder.find_font_file_by_fontname(family_name=self.__current_font_family, bold=self.__bold, italic=self.__italic)
            if not (self.__current_font_filepath):
                raise FileNotFoundError("Requested font ({font_family}) is not installed".format(font_family=self.__current_font_family))
        else:
            self.__current_font_filepath = self.__current_font_filepath or 'times.ttf'
        self.__font_base = ImageFont.truetype(font=self.__current_font_filepath, size=self.__current_font_size, encoding='unic')

        self.__current_text_vertical_alignment = vertical_alignment or self.__current_text_vertical_alignment or TextDrawer.TextAlignment.Top
        self.__current_text_horizontal_alignment = horizontal_alignment or self.__current_text_horizontal_alignment or TextDrawer.TextAlignment.Left
        self.__current_text_capitalization = capitalization or self.__current_text_capitalization or TextDrawer.CapitalizationModes.Normal

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

        self.color = color or self.color or 'white'

    def print_line(self, position, text:str):
        self.__print(position, text, real_print=True)

    def print_in_region(self, region, text:str, offset_borders:bool=True):
        return self.__print_in_region(region, text, offset_borders, real_print=True)

    def get_text_size(self, region, text:str, offset_borders:bool=True):
        return self.__print_in_region(region, text, offset_borders, real_print=False)

    def __print_in_region(self, region, text:str, offset_borders, real_print):
        if (offset_borders):
            x, y, w, h = region
        else:
            x, y, x2, y2 = region
            w = x2 - x
            h = y2 - y

        max_width = 0
        space_width, _ = self.__print(None, ' ', real_print=False)
        _, line_height = self.__print(None, 'LINE HEIGHT', real_print=False)
        paragraphs = []
        for paragraph in text.split('\n'):
            words = paragraph.split()
            lines = []
            line = { 'words': [], 'width': 0 }
            for word in words:
                word_width, _ = self.__print(None, word, real_print=False)
                if (not w or line['width'] + word_width + space_width <= w):
                    line['width'] += word_width + space_width
                    line['words'].append(word)
                else:
                    lines.append(line)
                    line = { 'words': [ word ], 'width': word_width }

                if (max_width < line['width']):
                    max_width = line['width']

            lines.append(line)
            paragraphs.append(lines)

        num_lines = sum(len(paragraph) for paragraph in paragraphs)
        total_height = int(num_lines * (1 + self.text_vertical_space_scale) * line_height + self.text_paragraph_vertical_space * (len(paragraphs) - 1))

        if (real_print):
            if (self.__current_text_vertical_alignment == TextDrawer.TextAlignment.Bottom):
                _y = y + h - total_height
            elif (self.__current_text_vertical_alignment == TextDrawer.TextAlignment.Center):
                _y = y + (h - total_height) // 2
            else:
                _y = y

            original_space_scale = self.text_space_scale
            for paragraph in paragraphs:
                for i in range(len(paragraph)):
                    line = paragraph[i]
                    last_line = (i + 1 == len(paragraph))

                    self.text_space_scale = original_space_scale
                    if (self.__current_text_horizontal_alignment == TextDrawer.TextAlignment.Right):
                        _x = x + w - line['width']
                    elif (self.__current_text_horizontal_alignment == TextDrawer.TextAlignment.Center):
                        _x = x + (w - line['width']) // 2
                    elif (self.__current_text_horizontal_alignment == TextDrawer.TextAlignment.Justify and not last_line and len(line['words']) > 0):
                        _x = x
                        new_space_width = (w - line['width']) / (len(line['words']) - 1)
                        self.text_space_scale = 1 + new_space_width / space_width
                    else:
                        _x = x

                    self.__print((_x, _y), ' '.join(line['words']), real_print=True)
                    _y += (1 + self.text_vertical_space_scale) * self.__current_font_size
                _y += self.text_paragraph_vertical_space

            self.text_space_scale = original_space_scale
        return max_width, total_height


    def __print(self, position, text: str, real_print:bool, debug_console_print:bool=False):
        x, y = position or (0, 0)
        max_height = 0

        _text = text
        if (self.__current_text_capitalization == TextDrawer.CapitalizationModes.UpperCase):
            _text = _text.upper()
        elif (self.__current_text_capitalization == TextDrawer.CapitalizationModes.LowerCase):
            _text = _text.lower()
        elif (self.__current_text_capitalization == TextDrawer.CapitalizationModes.Capitalize):
            _text = ' '.join(_word.capitalize() for _word in _text.split(' '))

        original_bold = self.__bold
        original_italic = self.__italic
        _continue = False

        for i in range(len(_text)):
            if (_continue):
                _continue = False
                continue
            if (i + 2 < len(_text)):
                if(_text[i:i+2] == '__'):
                    if (real_print):
                        self.set_font(italic=not self.__italic)
                    _continue = True
                    continue
                if (_text[i:i + 2] == '**'):
                    if (real_print):
                        self.set_font(bold=not self.__bold)
                    _continue = True
                    continue

            _char = _text[i]; _x = int(x); _y = int(y); _font = self.__font_base

            if (self.__current_text_capitalization == TextDrawer.CapitalizationModes.SmallCaps and _char != _char.upper()):
                # _, _new_size = self._drawer.textsize(_char, font=_font)
                _new_size = int(self.__current_font_size * 0.75)
                _char = _char.upper()
                _y += self.__current_font_size - _new_size
                _font = ImageFont.truetype(font=self.__current_font_filepath, size=_new_size, encoding='unic')

            w, h = self.__drawer.textsize(_char, font=_font)
            if (real_print):
                if (debug_console_print):
                    print(text[i], end='')
                self.__drawer.text((_x, _y), _char, self.color, font=_font)
            if (_char == ' '):
                x += w * self.text_space_scale
            else:
                x += w + self.text_character_separator_scale * self.__current_font_size
            if (max_height < h):
                max_height = h

        initial_x, _ = position or (0, 0)
        if (debug_console_print):
            print('', end='\n')
        if (real_print):
            self.set_font(bold=original_bold, italic=original_italic)
        return (x - initial_x, max_height)

def test():

    im = Image.open("compiler_images/hero_card_base_2_weapons.png")

    td = TextDrawer(im, font_size=285, bold=True)
    td.set_font_direct('BOD_B.TTF')
    td.set_font(capitalization=TextDrawer.CapitalizationModes.SmallCaps, character_separator_scale=0.2, horizontal_alignment=TextDrawer.TextAlignment.Center, vertical_alignment=TextDrawer.TextAlignment.Bottom)
    td.print_in_region((1200, 40, 3400, 240), 'Grey Seer', offset_borders=False)

    rules = \
    [
        "**Swarmed:** If you roll a 6 for the attack when using Vermintide, the affected target suffers D3 wounds instead of 1.",
        "**Warpstone Token:** After making an action roll to generate a Gray Seer's hero dice, you can choose to re-roll one of the dice. If you do so and roll 1, suffer a wound.",
        """**TRAITS:** Grey Seer is **Arcane** and **Chaotic**.
        **RENOWN:** If you roll 13 on your action roll, gain D6 renown.""",
    ]

    td = TextDrawer(im, font_size=90, color='black')
    td.set_font \
    (
        horizontal_alignment=TextDrawer.TextAlignment.Justify,
        vertical_alignment=TextDrawer.TextAlignment.Center,
        vertical_space_scale=0.15,
        paragraph_vertical_space=50,
    )
    y = 1330; dy = 80; light = True
    x1 = 365; x2 = 3233
    for rule in rules:
        _, _h = td.get_text_size((x1, y, x2, y), rule, offset_borders=False)
        _h += dy
        _drawer = ImageDraw.ImageDraw(im)
        if (light):
            _drawer.rectangle([(x1, y), (x2, y + _h)], fill='yellow')
        light = not light
        td.print_in_region((x1, y - 5, x2, y + _h - 5), rule, offset_borders=False)
        y += _h

    im.save('output/heroes/grey-seer.png')


if (__name__ == '__main__'):
    test()

