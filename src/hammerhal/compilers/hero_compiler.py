import json, os
from jsonschema import validate
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from hammerhal.text_drawer import TextDrawer
from hammerhal import ConfigLoader
from hammerhal.compilers import CompilerBase
from logging import getLogger
logger = getLogger('hammerhal.compilers.hero_compiler')

class HeroCompiler(CompilerBase):
    compiler_type = "hero"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def __get_font(fontfamily, size):
        return ImageFont.truetype("fonts/" + fontfamily + ".ttf", size)

    def compile(self):

        base = self.__prepare_base()
        if (not base):
            return None

        self.__print_name(base)
        self.__print_stats(base)
        self.__print_dice_space(base)
        self.__print_weapons(base)
        self.__print_rules(base)

        self.compiled = base
        return self.compiled

    def __prepare_base(self):
        filename = "{directory}{name}.png".format\
        (
            directory=ConfigLoader.get_from_config('sourcesDirectory', 'compilers'),
            name="hero_card_base_{n}_weapons".format(n=len(self.raw['weapons'])),
        )
        if (not os.path.isfile(filename)):
            logger.error("Cannot load hero card template with proper number of weapons: {n}".format(n=len(self.raw['weapons'])))
            return None
        base = Image.open(filename)
        if (self.raw.get('image')):
            filename = "{directory}{name}".format\
            (
                directory=ConfigLoader.get_from_config('rawDirectoryRoot'),
                name=self.raw['image'],
            )
            if (not os.path.isfile(filename)):
                logger.error("Cannot load hero image by path: '{path}' - no such file".format(path=self.raw['image']))
                return None
            base = self.insert_image_scaled(base_image=base, region=(0, 0, 1080, 1150), image_path=filename)
        return base
    def __print_name(self, base):
        # TODO: subtitle
        td = TextDrawer(base, font_size=int(285 * self.raw.get('titleFontSizeScale', 1.0)), bold=True)
        td.set_font_direct('BOD_B.TTF')
        td.set_font(capitalization=TextDrawer.CapitalizationModes.SmallCaps, horizontal_alignment=TextDrawer.TextAlignment.Center, vertical_alignment=TextDrawer.TextAlignment.Center)
        td.print_in_region((2400, 0, 0, 240), self.raw['name'], offset_borders=True)
    def __print_stats(self, base):
        td = TextDrawer(base, font_size=110, bold=True, font_family='Constantia', color='white')
        td.print_line((910, 750), "{move}".format(**self.raw['stats']))
        td.print_line((790, 950), "{save}+".format(**self.raw['stats']))
        td.print_line((990, 950), "{agility}+".format(**self.raw['stats']))
    def __print_dice_space(self, base):
        dice_section = self.raw.get('diceSpace', "default")
        if (dice_section == "default"):
            dice_section = ConfigLoader.get_from_config('compilerTypeSpecific/hero/defaultDiceSpace', 'compilers')

        total_dices_count = sum(_dice_type['count'] for _dice_type in dice_section)
        x1 = 1630; x2 = 3260
        _x = x1; _y = 533
        _dx = (x2 - x1) // (total_dices_count - 1)
        for _dice_type in dice_section:
            for i in range(_dice_type['count']):
                self.insert_image_centered(base_image=base, position=(_x, _y), image_path=self.sources_directory + _dice_type['image'])
                _x += _dx
    def __print_weapons(self, base):
        td = TextDrawer(base, font_size=70, color='black', bold=True)
        td.set_font(horizontal_alignment=TextDrawer.TextAlignment.Center, vertical_alignment=TextDrawer.TextAlignment.Center)

        self.insert_table \
        (
            vertical_columns = [ 1340, 2420, 2860, 3070, 3455 ],
            top = 760,
            cell_height = 110,
            data = self.raw['weapons'],

            body_row_template = [ "{name} ({cost}+)", "{range}", "{hit}+", "{damage}" ],
            body_text_drawer = td,
            body_row_interval = [ None, None, 60, 40 ][len(self.raw['weapons'])],
            body_capitalization = TextDrawer.CapitalizationModes.Capitalize,

            header_row = [ "WEAPON ACTIONS", "Range", "Hit", "Damage" ],
            header_text_drawer = td,
            header_row_interval = 70,
            header_capitalization = TextDrawer.CapitalizationModes.Normal,
        )
    def __print_rules(self, base):
        td = TextDrawer(base, font_size=90, color='black')
        td.set_font(horizontal_alignment=TextDrawer.TextAlignment.Justify, vertical_alignment=TextDrawer.TextAlignment.Center, vertical_space_scale=0.15)
        y = 1330; light = True
        gradient_base = self.__get_gradient_image()

        for ability in self.raw['abilities']:
            if (ability.get('cost', None)):
                text = "**{name} ({cost}+)**: {description}".format(**ability)
            else:
                text = "**{name}**: {description}".format(**ability)

            _h = self.__print_rules_block(base, td, y, text, light, gradient_base, dice_space=ability['diceSpace'])
            y += _h
            light = not light

        text_traits = "**TRAITS:** The {name} is **{trait_1}** and **{trait_2}**.".format(name=self.raw['name'], trait_1=self.raw['traits'][0].capitalize(), trait_2=self.raw['traits'][1].capitalize())
        text_renown = "**RENOWN:** {description}".format(description=self.raw['renown'])
        text = text_traits + '\n' + text_renown
        _h = self.__print_rules_block(base, td, y, text, light, gradient_base)
        y += _h
        light = not light

    def __get_gradient_image(self):

        r = 255; g = 255; b = 255; aMin = 0; aMax = 80
        im = Image.new("RGBA", size=(3600, 1), color=(r, g, b, aMin))

        x1 = 250
        x2 = 1200
        x3 = 2400
        x4 = 3400

        for i in range(x1, x2):
            a = int((aMax - aMin) * (i - x1) / (x2 - x1))
            im.putpixel((i, 0), (r, g, b, a))
        for i in range(x2, x3):
            a = aMax
            im.putpixel((i, 0), (r, g, b, a))
        for i in range(x3, x4):
            a = int(aMax - (aMax - aMin) * (i - x3) / (x4 - x3))
            im.putpixel((i, 0), (r, g, b, a))

        return im

    def __print_rules_block(self, base:Image.Image, text_drawer, y:int, text:str, light:bool, gradient_base:Image.Image, dice_space:bool=False):
        x1 = 365; x2 = 2933 if dice_space else 3233
        dy = 120

        _, _h = text_drawer.get_text_size((x1, y, x2, 0), text, offset_borders=False)

        if (dice_space):
            _, _h2 = self.get_image_size(self.sources_directory + "dice.png")
            _h = max(_h, _h2)
        _h += dy

        if (light):
            _w = gradient_base.width
            gradient = gradient_base.resize((_w, _h))
            base.paste(gradient, (0, y), gradient)

        if (dice_space):
            _x = 3260; _y = y + _h // 2
            self.insert_image_centered(base, (_x, _y), self.sources_directory + "dice.png")

        text_drawer.print_in_region((x1, y, x2, y + _h), text, offset_borders=False)
        return _h
