from PIL import Image, ImageDraw, ImageColor

from hammerdraw.compilers import CompilerModuleBase, CompilerError


class AdversaryRulesModule(CompilerModuleBase):
    module_name = "rules"
    behaviour_height = None

    def prepare(self):
        self.behaviour_height = hasattr(self.parent, 'behaviour_table_height') and self.parent.behaviour_table_height or 0
        return super().prepare()

    def get_size(self):
        _width = self.get_from_module_config('width')
        _height = self.get_from_module_config('heightMax') - self.behaviour_height
        size = (_width, _height)
        return size


    def _compile(self, base):
        td = self.get_text_drawer(base)

        y_min = 0
        y_max = self.height

        y = y_min
        column_number = 0
        for ability in self.parent.raw['abilities']:
            text = "**{name}:** {description}".format(**ability)
            if (ability.get('right', False)):
                y = y_min
                column_number += 1
            y, column_number = self.__print_rules_block(text_drawer=td, y=y, y_min=y_min, y_max=y_max, column_number=column_number, text=text)

        try:
            for ability in self.parent.raw.get('difficultyBonuses', []):
                text = "**Difficulty Bonus {name}:** {description}".format(**ability)
                if (ability.get('right', False)):
                    y = y_min
                    column_number += 1
                y, column_number = self.__print_rules_block(text_drawer=td, y=y, y_min=y_min, y_max=y_max, column_number=column_number, text=text)
        except AdversaryRulesModule.OutOfSpaceException as e:
            self.logger.warning("No space left on sheet for the difficulty bonus, it will be ignored")
        else:
            self.logger.info("Rules printed")

        return y

    class OutOfSpaceException(CompilerError):
        pass

    def __print_rules_block(self, text_drawer, column_number, y:int, y_min :int, y_max :int, text :str):
        x1 = self.get_from_module_config("textLeft");
        x2 = x1 + self.get_from_module_config("columnsWidth")
        dy = self.parent.raw.get('rulesSeparatorHeight', self.get_from_module_config("defaultRulesSeparatorHeight"))

        _, _h = text_drawer.get_text_size((x1, y, x2, 0), text, offset_borders=False)
        _h += dy

        if (y + _h > y_max):
            column_number += 1
            y = y_min

        if (column_number >= self.get_from_module_config("columnsCount")):
            message = "Not enough space left on the sheet to print the rule: {text}".format(text=text)
            self.logger.error(message)
            raise AdversaryRulesModule.OutOfSpaceException(message)

        _dx = (self.get_from_module_config("columnsWidth") + self.get_from_module_config("columnsSeparatorWidth")) * column_number
        x1 += _dx; x2 += _dx

        # -5 because of not correct intuitive of text while on print
        text_drawer.print_in_region((x1, y - 5, x2, y - 5 + _h), text, offset_borders=False)

        y += _h
        return y, column_number
