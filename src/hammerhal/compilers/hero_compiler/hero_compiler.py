from logging import getLogger

from hammerhal.compilers import CompilerBase
from hammerhal.compilers.modules import ImageModule, TextModule, StatsModule
from hammerhal.compilers.hero_compiler.dice_space_module import HeroDiceSpaceModule
from hammerhal.compilers.hero_compiler.rules_module import HeroRulesModule
from hammerhal.compilers.hero_compiler.weapons_module import HeroWeaponsModule
logger = getLogger('hammerhal.compilers.hero_compiler')

class HeroCompiler(CompilerBase):
    compiler_type = "hero"
    modules = \
    [
        ImageModule,
        (TextModule, { 'name': "name", 'scale_field': "titleFontSizeScale" } ),
        StatsModule,

        HeroDiceSpaceModule,
        HeroWeaponsModule,
        HeroRulesModule,
    ]
