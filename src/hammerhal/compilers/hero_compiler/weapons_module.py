from hammerhal.compilers.compiler_module_base import CompilerModuleBase
from hammerhal.text_drawer import TextDrawer


class HeroWeaponsModule(CompilerModuleBase):
    module_name = "weapons"

    def get_size(self):
        width = self.get_from_module_config("width")

        _cell_height = self.get_from_module_config("cellHeight")
        _weapons_count = len(self.parent.raw["weapons"])
        _body_row_interval = self.get_from_module_config("rowIntervalByCount")[len(self.parent.raw['weapons'])]
        _header_row_interval = self.get_from_module_config("headerRowInterval")
        height = _cell_height * (_weapons_count + 1) + _header_row_interval + _body_row_interval * (_weapons_count - 1)

        return width, height


    def _compile(self, base):
        td = self.get_text_drawer(base)

        self.parent.insert_table \
        (
            vertical_columns = self.get_from_module_config("verticalColumns"),
            top = 0,
            cell_height = self.get_from_module_config("cellHeight"),
            data = self.parent.raw['weapons'],

            body_row_template = [ "{name} ({cost}+)", "{range}", "{hit}+", "{damage}" ],
            body_text_drawer = td,
            body_row_interval = self.get_from_module_config("rowIntervalByCount")[len(self.parent.raw['weapons'])],
            body_capitalization = TextDrawer.CapitalizationModes.Capitalize,

            header_row = [ "WEAPON ACTIONS", "Range", "Hit", "Damage" ],
            header_text_drawer = td,
            header_row_interval = self.get_from_module_config("headerRowInterval"),
            header_capitalization = TextDrawer.CapitalizationModes.Normal,
        )
        self.logger.info("Weapon table printed")
