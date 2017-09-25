from PIL import Image
from logging import getLogger
from camel_case_switcher import dict_keys_camel_case_to_underscope

from hammerhal.config_loader import ConfigLoader
from hammerhal.text_drawer import TextDrawer
from hammerhal.compilers.compiler_error import CompilerError
from hammerhal.compilers.compiler_base import CompilerBase

class CompilerModuleBase:

    # These ones MUST be overwritten
    module_name = None

    # These ones MUST NOT be overwritten
    parent = None
    parent_type = None
    logger = None

    width = None
    height = None
    compiled = None

    def __init__(self, parent:CompilerBase, **kwargs):
        self.parent = parent
        self.parent_type = parent.compiler_type
        self.initialize(**kwargs)

        _logger_name = "hammerhal.compilers.{parentType}_compiler/{moduleName}_module".format \
        (
            parentType = self.parent_type,
            moduleName = self.module_name,
        )
        self.logger = getLogger(_logger_name)

        # Try config:
        path = 'compilerTypeSpecific/{parentType}/modules/{moduleName}'.format \
        (
            parentType = self.parent_type,
            moduleName = self.module_name,
        )
        if not (ConfigLoader.get_from_config(path, 'compilers')):
            message = "Module config not found: {parentType}/{moduleName}".format \
            (
                parentType = self.parent_type,
                moduleName = self.module_name,
            )

            self.logger.error(message)
            raise CompilerError(message)


    def initialize(self, **kwargs):
        pass

    def get_from_module_config(self, key):
        path = 'compilerTypeSpecific/{parentType}/modules/{moduleName}/{key}'.format \
        (
            parentType = self.parent_type,
            moduleName = self.module_name,
            key = key,
        )
        return ConfigLoader.get_from_config(path, 'compilers')

    def get_text_drawer(self, base:Image, font_prefix='font') -> TextDrawer:
        td = TextDrawer(base)
        font = self.get_from_module_config(font_prefix) or dict()
        font = dict_keys_camel_case_to_underscope(font)
        td.set_font(**font)
        return td


    def get_size(self):
        _width = self.get_from_module_config('width')
        _height = self.get_from_module_config('height')
        size = (_width, _height)
        return size

    def get_position(self):
        position = (self.get_from_module_config('positionX'), self.get_from_module_config('positionY'))
        return position

    def prepare(self):
        _size = self.get_size()
        base = Image.new('RGBA', _size, 0x00ffffff)
        self.width, self.height = _size
        return base

    def compile(self):
        base = self.prepare()
        self._compile(base)
        self.compiled = base
        return base
    def _compile(self, base:Image):
        raise NotImplementedError

    def insert(self, parent_base:Image.Image):
        _position = self.get_position()
        _image = self.compiled.convert('RGB')
        _mask = self.compiled
        parent_base.paste(_image, _position, _mask)