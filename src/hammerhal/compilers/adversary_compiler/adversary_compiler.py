from PIL import ImageDraw

from hammerhal.text_drawer import TextDrawer
from hammerhal.compilers import CompilerBase
from hammerhal.compilers.modules import ImageModule, TextModule, StatsModule, BehaviourTableModule
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
        StatsModule,
        (TextModule, { 'name': "description" } ),
        BehaviourTableModule,
        AdversaryRulesModule,
    ]

    def compile(self):

        base = self.prepare_base()
        if (not base):
            return None

        self.compile_modules(base)

        self.__print_weapons(base)

        self.compiled = base
        logger.info("Adversary compiled!")
        return self.compiled

    def __print_weapons(self, base):
        td = TextDrawer(base, font_size=80, color='black', bold=True)
        td.set_font(horizontal_alignment=TextDrawer.TextAlignment.Center, vertical_alignment=TextDrawer.TextAlignment.Center)

        self.insert_table \
        (
            vertical_columns = [ 2170, 3140, 3450, 3830, 4100, 4440 ],
            top = 1720,
            cell_height = 117,
            data = self.raw['weapons'],

            body_row_template = [ "{name}", "{dices}", "{range}", "{hit}+", "{damage}" ],
            body_text_drawer = td,
            body_row_interval = [ None, 80, 60, 40, None ][len(self.raw['weapons'])],
            body_capitalization = TextDrawer.CapitalizationModes.Capitalize,

            header_row = [ "WEAPON ACTIONS", "Dice", "Range", "Hit", "Damage" ],
            header_text_drawer = td,
            header_row_interval = 70,
            header_capitalization = TextDrawer.CapitalizationModes.Normal,
        )
        logger.info("Weapon table printed")
