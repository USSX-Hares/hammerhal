from hammerhal.compilers.compiler_module_base import CompilerModuleBase
from hammerhal.text_drawer import TextDrawer


class NameModule(CompilerModuleBase):
    module_name = "name"

    def _compile(self, base):
        # TODO: subtitle
        td = self.get_text_drawer(base)
        td.set_font(font_size=td.get_font()['font_size'] * self.parent.raw.get('titleFontSizeScale', 1.0))
        td.print_in_region((0, 0, self.width, self.height), self.parent.raw['name'], offset_borders=True)
        self.logger.info("Name printed")
