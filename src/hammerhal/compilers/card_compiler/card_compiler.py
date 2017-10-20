import json
from logging import getLogger

from hammerhal.compilers import CompilerBase
from hammerhal.compilers.card_compiler.affects_module import AffectsModule
from hammerhal.compilers.card_compiler.categories_module import CategoriesModule
from hammerhal.compilers.modules import TextModule, HeroRulesModule, WeaponsModule
logger = getLogger('hammerhal.compilers.card_compiler')

class CardCompiler(CompilerBase):
    modules = \
    [
        (TextModule, { 'name': "name", } ),
        (TextModule, { 'name': "type", } ),
        (TextModule, { 'name': "description", 'scale_field': "descriptionFontSizeScale", "multiline": True, 'after': None } ),
        (TextModule, { 'name': "effect", "multiline": True, 'after': 'description' } ),
        (HeroRulesModule, { 'after': 'effect', 'obstacles': True, } ),
        (WeaponsModule, { 'after': 'rules' } ),
        (AffectsModule, { 'after': 'weapons' } ),
        (CategoriesModule, { 'scale_field': "categoriesFontSizeScale" } ),
    ]
    compiler_type = "card"

    def search(self, type:str=None, set:str=None, ignore_dummies=True):
        result = super().search(ignore_dummies=ignore_dummies)
        if (type or set):
            _result = list()
            for filename in result:
                try:
                    _file = open(filename)
                    _json = json.load(_file)
                    _file.close()
                except (FileNotFoundError, PermissionError, IOError, json.JSONDecodeError):
                    logger.warning("{file}: Could not read json file, skipping...")
                else:
                    _type = _json.get("type")
                    if (type and _type != type):
                        continue

                    _set = _json.get("set")
                    if (set and _set != set):
                        continue

                    _result.append(filename)

            result = _result

        return result

    def _get_base_filename(self):
        return super()._get_base_filename() \
            .replace('{set}', str(self.raw['set'])) \
            .replace('{type}', str(self.raw['type'])) \
