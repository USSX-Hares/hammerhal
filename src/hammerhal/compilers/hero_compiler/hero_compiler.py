import json, os
from jsonschema import validate
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from hammerhal.text_drawer import TextDrawer
from hammerhal import ConfigLoader
from hammerhal.compilers import CompilerBase
from hammerhal.compilers.hero_compiler.name_module import HeroNameModule
from hammerhal.compilers.hero_compiler.stats_module import HeroStatsModule
from hammerhal.compilers.hero_compiler.dice_space_module import HeroDiceSpaceModule
from hammerhal.compilers.hero_compiler.weapons_module import HeroWeaponsModule
from hammerhal.compilers.hero_compiler.rules_module import HeroRulesModule

from logging import getLogger
logger = getLogger('hammerhal.compilers.hero_compiler')

class HeroCompiler(CompilerBase):
    compiler_type = "hero"
    modules = \
    [
        HeroNameModule,
        HeroStatsModule,
        HeroDiceSpaceModule,
        HeroWeaponsModule,
        HeroRulesModule,
    ]

    @staticmethod
    def __get_font(fontfamily, size):
        return ImageFont.truetype("fonts/" + fontfamily + ".ttf", size)

    def compile(self):

        base = self.__prepare_base()
        if (not base):
            return None

        self.compile_modules(base)

        self.compiled = base
        logger.info("Hero compiled!")
        return self.compiled

    def __prepare_base(self):
        filename = "{directory}{name}.png".format\
        (
            directory=self.sources_directory,
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
        logger.info("Image base prepared")
        return base
