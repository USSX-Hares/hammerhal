import json
from logging import getLogger

from hammerhal.compilers import CompilerBase
from hammerhal.compilers.modules import ImageModule, TextModule, StatsModule, WeaponsModule
from hammerhal.compilers.hero_compiler.dice_space_module import HeroDiceSpaceModule
from hammerhal.compilers.hero_compiler.rules_module import HeroRulesModule
logger = getLogger('hammerhal.compilers.card_compiler')

class CardCompiler(CompilerBase):
    modules = \
    [
    ]
    compiler_type = "card"

    def search(self, type:str=None, ignore_dummies=True):
        result = super().search(ignore_dummies=ignore_dummies)
        if (type):
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
                    if (_type == type):
                        _result.append(filename)

            result = _result

        return result