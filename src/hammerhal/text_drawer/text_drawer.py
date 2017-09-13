from PIL import Image, ImageDraw, ImageFont

class TextDrawer:

    class CapitalizationModes:
        Normal = 0
        UpperCase = 1
        AllCaps = 1
        LowerCase = 2
        NoCaps = 2
        Capitalize = 3
        SmallCaps = 4

    class TextAlignment:
        Left = 0
        Top = 0
        Center = 1
        Right = 2
        Bottom = 2
        Justify = 3

    _current_font_size = None
    _current_font_family = None
    _current_text_horizontal_alignment = None
    _current_text_vertical_alignment = None
    _current_text_capitalization = None
    _font_base = None
    _drawer : ImageDraw = None

    character_width_scale : float = None
    text_character_separator_scale = None
    text_vertical_space_scale = None
    text_space_scale = None
    color = None

    def __init__(self, im:Image.Image, font_family=None, font_size=None, color=None):
        self.set_font(font_family=font_family, font_size=font_size, color=color)
        self._drawer = ImageDraw.ImageDraw(im)

    def set_font(self, font_family=None, font_size=None, color=None, horizontal_alignment=None, vertical_alignment=None, character_width_scale=None, space_scale=None, vertical_space_scale=None, character_separator_scale=None, capitalization=None):
        self._current_font_size = font_size or self._current_font_size or 10
        self._current_font_family = font_family or self._current_font_family or 'times.ttf'
        self._font_base = ImageFont.truetype(font=self._current_font_family, size=self._current_font_size, encoding='unic')

        self._current_text_vertical_alignment = vertical_alignment or self._current_text_vertical_alignment or TextDrawer.TextAlignment.Top
        self._current_text_horizontal_alignment = horizontal_alignment or self._current_text_horizontal_alignment or TextDrawer.TextAlignment.Left
        self._current_text_capitalization = capitalization or self._current_text_capitalization or TextDrawer.CapitalizationModes.Normal

        self.text_space_scale = space_scale or self.text_space_scale or 1.0
        self.text_vertical_space_scale = vertical_space_scale or self.text_vertical_space_scale or 0.0
        self.text_character_separator_scale = character_separator_scale or self.text_character_separator_scale or 0.0
        self.character_width_scale = character_width_scale or self.character_width_scale or 1.0
        self.color = color or self.color or 'white'

    def get_text_size(self, text):
        pass

    def print_line(self, position, text:str):
        self.__print(position, text, real_print=True)

    def print_in_region(self, region, text:str, offset_borders:bool=True):
        if (offset_borders):
            x, y, w, h = region
        else:
            x, y, x2, y2 = region
            w = x2 - x
            h = y2 - y

        max_width = 0
        space_width, _ = self.__print(None, ' ', real_print=False)
        paragraphs = []
        for paragraph in text.split('\n'):
            words = paragraph.split()
            lines = []
            line = { 'words': [], 'width': 0 }
            for word in words:
                word_width, _ = self.__print(None, word, real_print=False)
                if (line['width'] + word_width + space_width <= w):
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
        total_height = (num_lines + (num_lines - 1) * self.text_vertical_space_scale) * self._current_font_size

        if (self._current_text_vertical_alignment == TextDrawer.TextAlignment.Bottom):
            _y = y + h - total_height
        elif (self._current_text_vertical_alignment == TextDrawer.TextAlignment.Center):
            _y = y + (h - total_height) // 2
        else:
            _y = y
        original_space_scale = self.text_space_scale
        for paragraph in paragraphs:
            for i in range(len(paragraph)):
                line = paragraph[i]
                last_line = (i + 1 == len(paragraph))

                self.text_space_scale = original_space_scale
                if (self._current_text_horizontal_alignment == TextDrawer.TextAlignment.Right):
                    _x = x + w - line['width']
                elif (self._current_text_horizontal_alignment == TextDrawer.TextAlignment.Center):
                    _x = x + (w - line['width']) // 2
                elif (self._current_text_horizontal_alignment == TextDrawer.TextAlignment.Justify and not last_line and len(line['words']) > 0):
                    _x = x
                    new_space_width = (w - line['width']) / (len(line['words']) - 1)
                    self.text_space_scale = 1 + new_space_width / space_width
                else:
                    _x = x



                self.__print((_x, _y), ' '.join(line['words']), real_print=True)
                _y += (1 + self.text_vertical_space_scale) * self._current_font_size

        self.text_space_scale = original_space_scale


    def __print(self, position, text: str, real_print:bool):
        x, y = position or (0, 0)
        max_height = 0

        _text = text
        if (self._current_text_capitalization == TextDrawer.CapitalizationModes.UpperCase):
            _text = _text.upper()
        elif (self._current_text_capitalization == TextDrawer.CapitalizationModes.LowerCase):
            _text = _text.lower()
        elif (self._current_text_capitalization == TextDrawer.CapitalizationModes.Capitalize):
            _text = _text.capitalize()

        for char in _text:
            _char = char; _x = int(x); _y = int(y); _font = self._font_base

            if (self._current_text_capitalization == TextDrawer.CapitalizationModes.SmallCaps and _char != _char.upper()):
                # _, _new_size = self._drawer.textsize(_char, font=_font)
                _new_size = int(self._current_font_size * 2 / 3)
                _char = _char.upper()
                _y += self._current_font_size - _new_size
                _font = ImageFont.truetype(font=self._current_font_family, size=_new_size, encoding='unic')

            w, h = self._drawer.textsize(_char, font=_font)
            if (real_print):
                print(char, end='')
                self._drawer.text((_x, _y), _char, self.color, font=_font)
            if (_char == ' '):
                x += w * self.text_space_scale
            else:
                x += w + self.text_character_separator_scale * self._current_font_size
            if (max_height < h):
                max_height = h

        initial_x, _ = position or (0, 0)
        if (real_print):
            print('', end='\n')
        return (x - initial_x, max_height)

def test():
    im = Image.open("compiler_images/hero_card_base.png")

    td = TextDrawer(im, font_family='BOD_R.TTF', font_size=200)
    td.set_font(capitalization=TextDrawer.CapitalizationModes.SmallCaps, character_separator_scale=0.2, horizontal_alignment=TextDrawer.TextAlignment.Center)
    td.print_in_region((1200, 100, 3600, 300), 'Grey Seer', offset_borders=False)

    rules = """Swarmed: If you roll a 6 for the attack when using Vermintide, the affected target suffers D3 wounds instead of 1.
    
    Warpstone Token: After making an action roll to generate a Gray Seer's hero dice, you can choose to re-roll one of the dice. If you do so and roll 1, suffer a wound.
    
    Traits: Grey Seer is Arcane and Chaotic.
    
    Renown: If you roll 13 on your action roll, gain D6 renown."""

    td = TextDrawer(im, font_family='times.ttf', font_size=100, color='black')
    td.set_font(horizontal_alignment=TextDrawer.TextAlignment.Justify)
    td.print_in_region((365, 1330, 3417, 2500), rules, offset_borders=False)

    im.save('output/heroes/grey-seer.png')


if (__name__ == '__main__'):
    test()

