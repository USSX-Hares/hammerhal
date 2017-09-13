import json
from jsonschema import validate
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

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
        filename = "{directory}{name}.png".format(directory=ConfigLoader.get_from_config('sourcesDirectory', 'compilers'), name="hero_card_base")
        base = Image.open(filename)
        draw = ImageDraw.Draw(base)

        left = 1200
        right = 3600
        top = 100
        bottom = 300

        font = ImageFont.truetype("BOD_R.TTF", bottom - top, encoding="unic")
        text = self.raw['name']
        text_width, _ = draw.textsize(text, font=font)
        draw.text(((left + right - text_width) / 2, top), text, (255, 255, 255), font=font)

        self.compiled = base
        return self.compiled
