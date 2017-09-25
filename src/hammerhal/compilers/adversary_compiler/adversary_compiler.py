from PIL import ImageDraw

from hammerhal.text_drawer import TextDrawer
from hammerhal.compilers import CompilerBase
from hammerhal.compilers.modules import ImageModule, TextModule, StatsModule, BehaviourTableModule, WeaponsModule
from hammerhal.compilers.adversary_compiler.rules_module import AdversaryRulesModule
from logging import getLogger
logger = getLogger('hammerhal.compilers.adversary_compiler')

class AdversaryCompiler(CompilerBase):
    compiler_type = "adversary"
    behaviour_table_height = None

    modules = \
    [
        ImageModule,
        (TextModule, { 'name': "name", 'scale_field': "titleFontSizeScale" } ),
        (TextModule, { 'name': "description" } ),
        StatsModule,
        WeaponsModule,
        BehaviourTableModule,
        AdversaryRulesModule,
    ]
