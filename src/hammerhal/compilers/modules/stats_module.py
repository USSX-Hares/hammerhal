from hammerhal.compilers.compiler_module_base import CompilerModuleBase
from hammerhal.text_drawer import TextDrawer


class StatsModule(CompilerModuleBase):
    module_name = "stats"

    def _compile(self, base):
        td = self.get_text_drawer(base)

        _stats = self.get_from_module_config('stats')
        for stat_name in _stats:
            _x = _stats[stat_name]['x']
            _y = _stats[stat_name]['y']
            _text_template = "{{{statName}}}{plusSymbol}".format(statName=stat_name, plusSymbol='+' if _stats[stat_name]['+'] else '')
            _text = _text_template.format(**self.parent.raw['stats'])
            td.print_line((_x, _y), _text)

        self.logger.info("Stats printed")
