from logging import getLogger

from hammerhal.compilers import CompilerBase
from hammerhal.compilers.modules import ImageModule, TextModule, StatsModule, WeaponsModule
from hammerhal.compilers.hero_compiler.dice_space_module import HeroDiceSpaceModule
from hammerhal.compilers.hero_compiler.rules_module import HeroRulesModule
logger = getLogger('hammerhal.compilers.hero_compiler')

class HeroCompiler(CompilerBase):
    modules = \
    [
        ImageModule,
        (TextModule, { 'name': "name", 'scale_field': "titleFontSizeScale" } ),
        StatsModule,
        WeaponsModule,

        HeroDiceSpaceModule,
        HeroRulesModule,
    ]
    compiler_type = "hero"
