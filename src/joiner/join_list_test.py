import unittest

from ddt import ddt, data
from joiner import join_list

@ddt
class CommonTests(unittest.TestCase):

    def do_test(self, x, estimated_result_1, estimated_result_2):
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, estimated_result_1)
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, estimated_result_2)
        
    @data \
    (
        None,
        list(),
        set(),
        dict(),
        '',
    )
    def test_empty_lists(self, input):
        self.do_test(input, '', '')

    @data \
    (
        ([ "first element" ], "first element", "first element"),
        ([ "first element", "second element" ], "first element, second element", "first element finally second element"),
        (["first element",  "second element", "third element"], "first element, second element, third element", "first element;second element finally third element"),
        ([ "first element", "second element", "third element", "fourth element" ], "first element, second element, third element, fourth element", "first element;second element;third element finally fourth element"),
        ([ "one", 2, 2.5, "three" ], "one, 2, 2.5, three", "one;2;2.5 finally three"),
    )
    def test_common_case(self, params):
        self.do_test(*params)
    
    @data \
    (
        ([ "one", 2, 2.5, "three" ], "!{0}!", "!one!, !2!, !2.5!, !three!", "!one!;!2!;!2.5! finally !three!"),
        ([ 16, 2, -42, 621 ], "{:x}", "10, 2, -2a, 26d", "10;2;-2a finally 26d"),
        ([ 16, 2, -42, 621 ], hex, "0x10, 0x2, -0x2a, 0x26d", "0x10;0x2;-0x2a finally 0x26d"),
        ([ 16, 2, -42, 621 ], lambda x: oct(abs(x)), "0o20, 0o2, 0o52, 0o1155", "0o20;0o2;0o52 finally 0o1155"),
        ([ "first element", "second element", "third element", "fourth element" ], lambda x: "**{0}**".format(x.capitalize()), "**First element**, **Second element**, **Third element**, **Fourth element**", "**First element**;**Second element**;**Third element** finally **Fourth element**"),
    )
    def test_formatter(self, params):
        x, formatter, estimated_result_1, estimated_result_2 = params
        result = join_list(x, formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, estimated_result_1)
        result = join_list(x, ';', ' finally ', formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, estimated_result_2)

class CombatTestingCase(unittest.TestCase):
    def test_card_categories_living_fortress(self):
        categories = [ "armour" ]
        name = "Living Fortress"

        categories_str = join_list(categories, last_separator=' and ', formatter=lambda s: "**{0}**".format(s.capitalize()))
        result = "{name} is {categories}.".format(name=name, categories=categories_str)
        print('"{:}"'.format(result))
        self.assertEqual(result, "Living Fortress is **Armour**.")

    def test_card_categories_ring_of_celerity(self):
        categories= ["move", "dices", "reusable"]
        name = "Ring of Celerity"

        categories_str = join_list(categories, last_separator=' and ', formatter=lambda s: "**{0}**".format(s.capitalize()))
        result = "{name} is {categories}.".format(name=name, categories=categories_str)
        print('"{:}"'.format(result))
        self.assertEqual(result, "Ring of Celerity is **Move**, **Dices** and **Reusable**.")

if __name__ == '__main__':
    unittest.main()
