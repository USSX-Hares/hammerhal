import os
from PIL import Image
from PIL import ImageFont

from hammerhal import ConfigLoader
from hammerhal.compilers import CompilerBase
from hammerhal.compilers.image_module import ImageModule
from hammerhal.compilers.hero_compiler.name_module import HeroNameModule
from hammerhal.compilers.hero_compiler.stats_module import HeroStatsModule
from hammerhal.compilers.hero_compiler.dice_space_module import HeroDiceSpaceModule
from hammerhal.compilers.hero_compiler.weapons_module import HeroWeaponsModule
from hammerhal.compilers.hero_compiler.rules_module import HeroRulesModule

from logging import getLogger
logger = getLogger('hammerhal.compilers.hero_compiler')

class HeroCompiler(CompilerBase):
    compiler_type = "hero"
    modules = \
    [
        ImageModule,
        HeroNameModule,
        HeroStatsModule,
        HeroDiceSpaceModule,
        HeroWeaponsModule,
        HeroRulesModule,
    ]
