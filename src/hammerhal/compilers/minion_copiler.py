from logging import getLogger

from hammerhal.compilers import CompilerBase
from hammerhal.compilers.modules import HeroDiceSpaceModule, ImageModule, TextModule, StatsModule, WeaponsModule, HeroRulesModule, BehaviourTableModule
logger = getLogger('hammerhal.compilers.minion_compiler')

class MinionCompiler(CompilerBase):
    modules = \
    [
        ImageModule,
        (TextModule, { 'name': "name", 'scale_field': "titleFontSizeScale" } ),
        StatsModule,
        WeaponsModule,

        HeroDiceSpaceModule,
        HeroRulesModule,
        BehaviourTableModule,
    ]
    compiler_type = "minion"

    def _get_base_filename(self):
        return super()._get_base_filename() \
            .replace('{weaponsCount}', str(len(self.raw['weapons'])))
