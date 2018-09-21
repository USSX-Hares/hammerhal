from hammerdraw.compilers.modules import TextModule
from hammerdraw.text_drawer.text_funcs import capitalize_first
from joiner.join_list import join_list


class CategoriesModule(TextModule):

    def initialize(self, **kwargs):
        super(CategoriesModule, self).initialize(name='categories', field='categories', multiline=True, **kwargs)

    def _compile(self, base):
        categories = self.parent.raw.get(self.raw_field) or []
        item_type = self.parent.raw.get('itemType')
        if (item_type):
            categories = [ item_type ] + categories

        name = self.parent.raw.get('name')
        if (not categories):
            return 0

        # categories_str = join_list(categories, last_separator=' and ', formatter=lambda s: "**{0}**".format(s.capitalize()))
        # text = "{name} is {categories}.".format(name=name, categories=categories_str)
        text = join_list(categories, formatter=lambda s: "**{0}**".format(capitalize_first(s)))
        return self._print(base, text)

    def _create_generator_tab_content(self):
        raise NotImplementedError
