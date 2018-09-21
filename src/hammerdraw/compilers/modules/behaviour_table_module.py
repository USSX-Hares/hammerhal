from PIL import Image, ImageDraw, ImageColor

from hammerdraw.compilers import CompilerModuleBase, CompilerError
from hammerdraw import get_color


class BehaviourTableModule(CompilerModuleBase):
    module_name = "behaviour"
    raw_body_font_size_scale_field = "behaviourBodyFontSizeScale"
    raw_header_font_size_scale_field = "behaviourHeaderFontSizeScale"

    def get_size(self):
        _width = self.get_from_module_config('width')
        _height = self.get_from_module_config('heightMax')
        size = (_width, _height)
        return size

    def _compile(self, base):
        td = self.get_text_drawer(base, font_prefix='fonts/tableBody')
        _scale = self.parent.raw.get(self.raw_body_font_size_scale_field, 1.0)
        if (_scale != 1.0):
            td_font = td.get_font()
            td.set_font(font_size=td_font['font_size'] * _scale)
        
        th = self.get_text_drawer(base, font_prefix='fonts/tableHeader')
        _scale = self.parent.raw.get(self.raw_header_font_size_scale_field, 1.0)
        if (_scale != 1.0):
            th_font = th.get_font()
            th.set_font(font_size=th_font['font_size'] * _scale)

        behaviour_table_height = self.parent.insert_table \
        (
            vertical_columns = self.get_from_module_config("tableVerticalColumns"),
            top = -self.height - (self.get_from_module_config("tableBottomOffset") + self.get_from_module_config("borderBottom")),
            cell_height = 0,
            data = self.parent.raw['behaviourTable']['table'],
            
            body_row_template = [ "$$HA_C **{roll}**", "**{name}:** {description}" ],
            body_text_drawer = td,
            body_row_interval = self.get_from_module_config("tableBodyRowInterval"),
            
            header_row = [ "$$HA_C " + self.parent.raw['behaviourTable'].get('dices', "D6").upper(), "Actions" ],
            header_text_drawer = th,
            header_bold = True,
        )
        
        x1 = self.get_from_module_config("borderLeft")
        x2 = self.get_from_module_config("borderRight")
        y2 = self.height + self.get_from_module_config("borderBottom")
        y1 = y2 + self.get_from_module_config("tableBottomOffset") - behaviour_table_height + self.get_from_module_config("borderTopOffset")
        rectangle_width = self.get_from_module_config("borderWidth")
        drawer = ImageDraw.ImageDraw(base)
        
        td = self.get_text_drawer(base, font_prefix='fonts/title')
        table_caption = self.parent.raw['behaviourTable'].get('title', "Behaviour Table")
        td.print_in_region((x1, y1, x2, y1 + self.get_from_module_config("titleHeight")), text=table_caption, offset_borders=False)
        
        for i in range(rectangle_width):
            _i = i - rectangle_width // 2
            _x1 = x1 + _i
            _y1 = y1 + _i
            _x2 = x2 - _i
            _y2 = y2 - _i
            drawer.rectangle([(_x1, _y1), (_x2, _y2)], outline=get_color(self.get_from_module_config("borderColor")))
        behaviour_table_height -= self.get_from_module_config("borderTopOffset")

        self.logger.info("Behaviour table printed")
        if (hasattr(self.parent, 'behaviour_table_height')):
            self.parent.behaviour_table_height = behaviour_table_height

        return behaviour_table_height
