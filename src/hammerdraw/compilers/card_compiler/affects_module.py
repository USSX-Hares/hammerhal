from hammerdraw.modules import TextModule
from hammerdraw.text_drawer.text_funcs import capitalize_first

from joiner.join_list import join_list

class AffectsModule(TextModule):

    def initialize(self, **kwargs):
        super(AffectsModule, self).initialize(name='affects', field='additionalEffect', multiline=True, **kwargs)

    def _compile(self, base):
        bonus_text = self.parent.raw.get(self.raw_field)
        if (not bonus_text):
            return 0

        traits_str = join_list(self.parent.raw.get('affects'), last_separator=' or ', formatter=lambda s: "**{0}**".format(capitalize_first(s)))
        text = "If your hero is {traits}, {text}".format(traits=traits_str, text=bonus_text)
        return self._print(base, text)

