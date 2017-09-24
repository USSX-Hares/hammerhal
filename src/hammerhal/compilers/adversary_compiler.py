import json, os
from jsonschema import validate
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from hammerhal.text_drawer import TextDrawer
from hammerhal import ConfigLoader
from hammerhal.compilers import CompilerBase, CompilerException
from logging import getLogger
logger = getLogger('hammerhal.compilers.adversary_compiler')

class AdversaryCompiler(CompilerBase):
    compiler_type = "adversary"

    @staticmethod
    def __get_font(fontfamily, size):
        return ImageFont.truetype("fonts/" + fontfamily + ".ttf", size)

    def compile(self):

        base = self.__prepare_base()
        if (not base):
            return None

        self.__print_name(base)
        self.__print_description(base)
        self.__print_stats(base)
        self.__print_weapons(base)
        behaviour_height = self.__print_behaviour_table(base)
        try:
            self.__print_rules(base, behaviour_height=behaviour_height)
        except AdversaryCompiler.OutOfSpaceException:
            return None

        self.compiled = base
        logger.info("Adversary compiled!")
        return self.compiled

    def __prepare_base(self):
        filename = "{directory}{name}.png".format\
        (
            directory=self.sources_directory,
            name="adversary_sheet_base_{n}_weapons".format(n=len(self.raw['weapons'])),
        )
        if (not os.path.isfile(filename)):
            logger.error("Cannot load adversary card template with proper number of weapons: {n}".format(n=len(self.raw['weapons'])))
            return None
        base = Image.open(filename)
        if (self.raw.get('image')):
            filename = "{directory}{name}".format\
            (
                directory=ConfigLoader.get_from_config('rawDirectoryRoot'),
                name=self.raw['image'],
            )
            if (not os.path.isfile(filename)):
                logger.error("Cannot load adversary image by path: '{path}' - no such file".format(path=self.raw['image']))
                return None
            base = self.insert_image_scaled(base_image=base, region=(204, 871, 1470, 1470), image_path=filename)

        logger.info("Image base prepared")
        return base

    def __print_name(self, base):
        td = TextDrawer(base, font_size=int(285 * self.raw.get('titleFontSizeScale', 1.0)), bold=True)
        td.set_font_direct('BOD_B.TTF')
        td.set_font(capitalization=TextDrawer.CapitalizationModes.SmallCaps, horizontal_alignment=TextDrawer.TextAlignment.Center, vertical_alignment=TextDrawer.TextAlignment.Center)
        td.print_in_region((1596, 810, 2655, 350), self.raw['name'], offset_borders=True)
        logger.info("Name printed")
    def __print_description(self, base):
        td = TextDrawer(base, font_size=104, bold=True, color='black')
        td.set_font(horizontal_alignment=TextDrawer.TextAlignment.Justify, vertical_alignment=TextDrawer.TextAlignment.Center)
        td.print_in_region((1930, 1200, 4400, 1600), self.raw['description'], offset_borders=False)
        logger.info("Description printed")
    def __print_stats(self, base):
        td = TextDrawer(base, font_size=110, bold=True, font_nane='Constantia', color='white')
        td.print_line((1700, 1830), "{move}".format(**self.raw['stats']))
        td.print_line((1575, 2030), "{vigour}".format(**self.raw['stats']))
        td.print_line((1770, 2030), "{agility}+".format(**self.raw['stats']))
        logger.info("Stats printed")
    def __print_weapons(self, base):
        td = TextDrawer(base, font_size=80, color='black', bold=True)
        td.set_font(horizontal_alignment=TextDrawer.TextAlignment.Center, vertical_alignment=TextDrawer.TextAlignment.Center)

        self.insert_table \
        (
            vertical_columns = [ 2170, 3140, 3450, 3830, 4100, 4440 ],
            top = 1720,
            cell_height = 117,
            data = self.raw['weapons'],

            body_row_template = [ "{name}", "{dices}", "{range}", "{hit}+", "{damage}" ],
            body_text_drawer = td,
            body_row_interval = [ None, 80, 60, 40, None ][len(self.raw['weapons'])],
            body_capitalization = TextDrawer.CapitalizationModes.Capitalize,

            header_row = [ "WEAPON ACTIONS", "Dice", "Range", "Hit", "Damage" ],
            header_text_drawer = td,
            header_row_interval = 70,
            header_capitalization = TextDrawer.CapitalizationModes.Normal,
        )
        logger.info("Weapon table printed")
    def __print_behaviour_table(self, base):
        td = TextDrawer(base, font_size=80, color='black')
        td.set_font(horizontal_alignment=TextDrawer.TextAlignment.Justify, vertical_alignment=TextDrawer.TextAlignment.Top, vertical_space_scale=0.2875)
        th = TextDrawer(base, font_size=105, color='black')
        th.set_font(horizontal_alignment=TextDrawer.TextAlignment.Justify, vertical_alignment=TextDrawer.TextAlignment.Center)

        behaviour_table_height = self.insert_table \
        (
            vertical_columns = [ 600, 950, 4420 ],
            top = -5930,
            cell_height = 0,
            data = self.raw['behaviourTable']['table'],

            body_row_template = [ "$$HA_C **{roll}", "**{name}:** {description}" ],
            body_text_drawer = td,
            body_row_interval = 45,

            header_row = [ "$$HA_C " + self.raw['behaviourTable'].get('dices', "D6").upper(), "Actions" ],
            header_text_drawer = th,
            header_bold = True,
        )

        x1 = 580; y1 = 5930 - behaviour_table_height - 185
        x2 = 4470; y2 = 6045
        rectangle_width = 8
        drawer = ImageDraw.ImageDraw(base)

        td = TextDrawer(base, font_size=125, color='black', bold=True)
        td.set_font(horizontal_alignment=TextDrawer.TextAlignment.Center, vertical_alignment=TextDrawer.TextAlignment.Center, capitalization=TextDrawer.CapitalizationModes.AllCaps)
        td.print_in_region((x1, y1, x2, y1 + 240), text='Behaviour Table', offset_borders=False)

        for i in range(rectangle_width):
            _i = i - rectangle_width // 2
            _x1 = x1 + _i
            _y1 = y1 + _i
            _x2 = x2 - _i
            _y2 = y2 - _i
            # color in ABGR
            drawer.rectangle([(_x1, _y1), (_x2, _y2)], outline=0xff9795ab)
        behaviour_table_height += 185

        logger.info("Behaviour table printed")
        return behaviour_table_height
    def __print_rules(self, base, behaviour_height):
        td = TextDrawer(base, font_size=90, color='black')
        td.set_font \
        (
            horizontal_alignment=TextDrawer.TextAlignment.Justify,
            vertical_alignment=TextDrawer.TextAlignment.Center,
            vertical_space_scale=0.1666,
            paragraph_vertical_space=50,
        )
        y_min = 2540
        # 5930 is bottom edge of behaviour table
        # 350 is distance between bottom edge of rules region and behaviour table
        y_max = 5930 - behaviour_height - 100

        y = y_min
        right = False
        for ability in self.raw['abilities']:
            text = "**{name}:** {description}".format(**ability)
            y, right = self.__print_rules_block(text_drawer=td, y=y, y_min=y_min, y_max=y_max, right=ability.get('right', right), text=text)

        try:
            for ability in self.raw.get('difficultyBonuses', []):
                text = "**Difficulty Bonus {name}:** {description}".format(**ability)
                y, right = self.__print_rules_block(text_drawer=td, y=y, y_min=y_min, y_max=y_max, right=ability.get('right', right), text=text)
        except AdversaryCompiler.OutOfSpaceException as e:
            logger.warning("No space left on sheet for the difficulty bonus, it will be ignored")
        else:
            logger.info("Rules printed")


    class OutOfSpaceException(CompilerException):
        pass

    def __print_rules_block(self, text_drawer, right, y:int, y_min:int, y_max:int, text:str):
        x1 = 580; x2 = 2400
        dy = self.raw.get('rulesSeparatorHeight', 200)

        _, _h = text_drawer.get_text_size((x1, y, x2, 0), text, offset_borders=False)
        _h += dy

        if (y + _h > y_max):
            if (not right):
                right = True
                y = y_min
            else:
                message = "Not enough space left on the sheet to print the rule: {text}".format(text=text)
                logger.error(message)
                raise AdversaryCompiler.OutOfSpaceException(message)
        if (right):
            x1 += 2000; x2 += 2000

        # -5 because of not correct intuitive of text while on print
        text_drawer.print_in_region((x1, y - 5, x2, y - 5 + _h), text, offset_borders=False)

        y += _h
        return y, right
