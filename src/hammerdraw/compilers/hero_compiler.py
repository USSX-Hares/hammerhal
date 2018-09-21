from logging import getLogger

from hammerdraw.compilers import CompilerBase
from hammerdraw.modules.dice_space_module import HeroDiceSpaceModule
from hammerdraw.modules import ImageModule, TextModule, StatsModule, WeaponsModule, HeroRulesModule
logger = getLogger('hammerdraw.compilers.hero_compiler')

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

    def _get_base_filename(self):
        return super()._get_base_filename() \
            .replace('{weaponsCount}', str(len(self.raw['weapons'])))
