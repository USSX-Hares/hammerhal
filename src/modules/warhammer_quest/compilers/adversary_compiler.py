from hammerdraw.compilers import CompilerBase
from modules.core.core import ImageModule, TextModule
from modules.warhammer_quest import StatsModule, BehaviourTableModule, WeaponsModule, AdversaryRulesModule
from logging import getLogger
logger = getLogger('hammerdraw.compilers.adversary_compiler')

class AdversaryCompiler(CompilerBase):
    compiler_type = "adversary"
    behaviour_table_height = None

    modules = \
    [
        ImageModule,
        (TextModule, { 'name': "name", 'scale_field': "titleFontSizeScale" } ),
        (TextModule, { 'name': "description", 'scale_field': "descriptionFontSizeScale", 'multiline': True } ),
        StatsModule,
        WeaponsModule,
        BehaviourTableModule,
        AdversaryRulesModule,
    ]

    def _get_base_filename(self):
        return super()._get_base_filename() \
            .replace('{weaponsCount}', str(len
        (self.raw['weapons'])))
