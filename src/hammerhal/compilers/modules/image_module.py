from hammerhal.compilers.compiler_module_base import CompilerModuleBase
from hammerhal.config_loader import ConfigLoader
import os


class ImageModule(CompilerModuleBase):
    module_name = "image"
    image_path = None

    def initialize(self, **kwargs):
        self.image_path = None

    def _compile(self, base):
        if (not self.parent.raw.get('image')):
            self.image_path = None
            return

        filename = "{directory}{name}".format\
        (
            directory=ConfigLoader.get_from_config('rawDirectoryRoot'),
            name=self.parent.raw['image'],
        )
        if (not os.path.isfile(filename)):
            self.logger.error("Cannot load {type} image by path: '{path}' - no such file".format(type=self.parent.compiler_type, path=self.parent.raw['image']))
            self.image_path = None
            return

        self.image_path = filename
        self.logger.info("Image verified")

    def insert(self, parent_base):
        if (not self.image_path):
            return

        _x, _y = self.get_position()
        self.parent.insert_image_scaled(base_image=parent_base, region=(_x, _y, self.width, self.height), image_path=self.image_path)
        self.logger.info("Image inserted")
