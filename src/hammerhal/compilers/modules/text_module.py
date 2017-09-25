from hammerhal.compilers.compiler_module_base import CompilerModuleBase
from hammerhal.text_drawer import TextDrawer


class TextModule(CompilerModuleBase):
    module_name = None
    raw_field = None
    raw_font_size_scale_field = None

    def initialize(self, name:str, field:str=None, prefix:str="", scale_field:str=None, **kwargs):
        self.module_name = name
        self.raw_field = prefix + (field or name)
        if (scale_field):
            self.raw_font_size_scale_field = prefix + scale_field

    def _compile(self, base):
        td = self.get_text_drawer(base)
        if (self.raw_font_size_scale_field):
            _scale = self.parent.raw.get(self.raw_font_size_scale_field, 1.0)
            if (_scale != 1.0):
                td.set_font(font_size=td.get_font()['font_size'] * _scale)

        td.print_in_region((0, 0, self.width, self.height), self.parent.raw[self.raw_field], offset_borders=True)
        self.logger.info("{type} printed".format(type=self.module_name.capitalize()))
