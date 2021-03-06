from PIL import Image, ImageDraw, ImageColor

from hammerhal import get_color
from hammerhal.compilers.compiler_module_base import CompilerModuleBase


class HeroRulesModule(CompilerModuleBase):
    module_name = "rules"

    def _compile(self, base):
        td = self.get_text_drawer(base)
        y = 0; light = not(len(self.parent.raw['abilities']) & 1)
        gradient_base = self.__get_gradient_image()

        for ability in self.parent.raw['abilities']:
            if (ability.get('cost', None)):
                text = "**{name} ({cost}+):** {description}".format(**ability)
            else:
                text = "**{name}:** {description}".format(**ability)

            _h = self.__print_rules_block(base, td, y, text, light, gradient_base, dice_space=ability['diceSpace'])
            y += _h
            light = not light

        text_traits = "**TRAITS:** The {name} is **{trait_1}** and **{trait_2}**.".format(name=self.parent.raw['name'], trait_1=self.parent.raw['traits'][0].capitalize(), trait_2=self.parent.raw['traits'][1].capitalize())
        text_renown = "**RENOWN:** {description}".format(description=self.parent.raw['renown'])
        text = text_traits + '\n' + text_renown
        _h = self.__print_rules_block(base, td, y, text, light, gradient_base)
        y += _h
        light = not light
        self.logger.info("Rules printed")

    def __get_gradient_image(self):

        _gradient_section = self.get_from_module_config('gradient')
        if (not isinstance(_gradient_section, list)):
            raise TypeError("Gradient section should be a list.")
        if (len(_gradient_section) < 2):
            raise IndexError("Gradient section should have at least 2 points.")

        im = Image.new("RGBA", size=(_gradient_section[-1]['position'], 1))

        for i in range(len(_gradient_section) - 1):
            x1 = _gradient_section[i]['position']
            x2 = _gradient_section[i+1]['position']

            _color1 = get_color(_gradient_section[i]['color'])
            _color2 = get_color(_gradient_section[i+1]['color'])

            r1, g1, b1, a1 = _color1
            r2, g2, b2, a2 = _color2
            for i in range(x1, x2):
                offset = (i - x1) / (x2 - x1)
                r = int(r1 + (r2 - r1) * offset)
                g = int(g1 + (g2 - g1) * offset)
                b = int(b1 + (b2 - b1) * offset)
                a = int(a1 + (a2 - a1) * offset)
                im.putpixel((i, 0), (r, g, b, a))

        return im

    def __print_rules_block(self, base:Image, text_drawer, y:int, text:str, light:bool, gradient_base:Image, dice_space:bool=False):
        x1 = self.get_from_module_config('textLeft'); x2 = self.get_from_module_config('textWidthWithDice') if dice_space else self.get_from_module_config('textWidthNoDice')
        dy = self.parent.raw.get('rulesSeparatorHeight', self.get_from_module_config("defaultRulesSeparatorHeight"))

        _, _h = text_drawer.get_text_size((x1, y, x2, 0), text, offset_borders=False)

        if (dice_space):
            _, _h2 = self.parent.get_image_size(self.parent.sources_directory + "dice.png")
            _h = max(_h, _h2)
        _h += dy

        if (light):
            _w = gradient_base.width
            gradient = gradient_base.resize((_w, _h))
            _gradient = gradient.convert('RGB')

            base.paste(_gradient, (0, y), gradient)

        if (dice_space):
            _x = self.get_from_module_config("dicePosition"); _y = y + _h // 2
            self.parent.insert_image_centered(base, (_x, _y), self.parent.sources_directory + self.get_from_module_config("diceImage"))

        # -5 because of not correct intuitive of text while on print
        text_drawer.print_in_region((x1, y - 5, x2, y - 5 + _h), text, offset_borders=False)
        return _h
