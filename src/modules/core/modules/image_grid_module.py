import itertools
from typing import List

from hammerdraw.module_base import ModuleBase


class ImageGridModule(ModuleBase):
    module_name: str = 'image_grid'
    raw_field: str = None
    rows: int = None
    columns: int = None
    image_list: List[str] = None

    def initialize(self, *, image_list: List[str] = None, raw_filed: str = None, rows: int = None, columns: int = None, **kwargs):
        super().initialize(**kwargs)
        
        self.rows = rows or self.get_from_module_config('rows')
        self.columns = columns or self.get_from_module_config('columns')
        self.raw_field = raw_filed
        self.image_list = image_list
    
    def _compile(self, base):
        image_list: List[str] = self.parent.raw.get(self.raw_field) if (self.image_list is None) else self.image_list
        _dx = self.width // self.columns
        _dy = self.height // self.rows
        
        _x0 = _dx // 2
        _y0 = _dy // 2
        for _img, (j, i) in zip(image_list, itertools.product(range(self.rows), range(self.columns))):
             # = _comb[0]
            _x = _x0 + _dx * i
            _y = _y0 + _dy * j
            self.logger.debug(f"Printing image '{_img}' to the position ({i};{j}) [ ({_x};{_y}) ]." )
            self.parent.insert_image_centered(base_image=base, position=(_x, _y), image_path=_img)
        
        self.logger.info("Grid printed")
        return 0
