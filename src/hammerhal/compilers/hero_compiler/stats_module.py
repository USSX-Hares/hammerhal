from hammerhal.compilers.compiler_module_base import CompilerModuleBase
from hammerhal.text_drawer import TextDrawer


class HeroStatsModule(CompilerModuleBase):
    module_name = "stats"

    def _compile(self, base):
        td = self.get_text_drawer(base)
        td.print_line((self.get_from_module_config('moveX'), self.get_from_module_config('moveY')), "{move}".format(**self.parent.raw['stats']))
        td.print_line((self.get_from_module_config('saveX'), self.get_from_module_config('saveY')), "{save}+".format(**self.parent.raw['stats']))
        td.print_line((self.get_from_module_config('agilityX'), self.get_from_module_config('agilityY')), "{agility}+".format(**self.parent.raw['stats']))
        self.logger.info("Stats printed")
