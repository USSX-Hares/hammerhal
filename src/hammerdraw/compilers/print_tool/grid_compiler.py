import math
from typing import List

from hammerdraw.compilers import CompilerBase
from modules.core.core import ImageGridModule
from logging import getLogger
logger = getLogger('hammerdraw.compilers.print_tool.grid_compiler')

class GridCompiler(CompilerBase):
    compiler_type = "grid-compiler"
    
    is_controller: bool
    
    # Controller:
    children: List['GridCompiler']
    images: List[str]
    
    modules = \
    [
        (ImageGridModule, dict(raw_filed='images')),
    ]
    
    def __init__(self, *, is_controller: bool = True):
        self.is_controller = is_controller
        super().__init__()
    
    def open(self, *args, **kwargs):
        kwargs['ignore_schema'] = True
        result = super().open(*args, **kwargs)
        
        if (not self.is_controller):
            return result
        
        self.images = self.find_images()
        rows: int = self.get_from_compiler_config('modules/image_grid/rows')
        cols: int = self.get_from_compiler_config('modules/image_grid/columns')
        
        max_per_page = rows * cols
        num_pages = math.ceil(len(self.images) / max_per_page)
        self.children = [ ]
        for i in range(num_pages):
            _child = GridCompiler(is_controller=False)
            _child.open(*args, **kwargs)
            _child.raw['number'] = i + 1
            _child.raw['images'] = self.images[max_per_page*i : max_per_page*(i+1)]
            _child.raw['name'] = self.raw['name'].format(**_child.raw)
            
            self.children.append(_child)
        
        return result
    
    def compile(self, *args, **kwargs):
        if (self.is_controller):
            result = True
            for _child in self.children:
                result = result and _child.compile(*args, **kwargs)
            return result
        else:
            return super().compile(*args, **kwargs)
    
    def save_compiled(self, *args, **kwargs):
        if (self.is_controller):
            result = True
            for _child in self.children:
                result = result and _child.save_compiled(*args, **kwargs)
            return result
        else:
            return super().save_compiled(*args, **kwargs)
    
    def find_images(self):
        if (self.raw.get('repeat', True)):
            rows: int = self.get_from_compiler_config('modules/image_grid/rows')
            cols: int = self.get_from_compiler_config('modules/image_grid/columns')
            
            return [ self.raw['imagePath'] ] * (rows * cols) 
        
        else:
            return self.search(extension='png', directory=self.raw['imagePath'])
