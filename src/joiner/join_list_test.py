import unittest

from joiner import join_list
class EmptyListCase(unittest.TestCase):
    def test_none(self):
        x = None
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "")

    def test_empty_list(self):
        x = []
        result = join_list([])
        print('"{:}"'.format(result))
        self.assertEqual(result, "")
        result = join_list([], ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "")

    def test_empty_set(self):
        x = set()
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "")

    def test_empty_dict(self):
        x = dict()
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "")

    def test_empty_str(self):
        x = ''
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "")

class CommonCase(unittest.TestCase):
    def test_1(self):
        x = [ "first element" ]
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "first element")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "first element")

    def test_2(self):
        x = [ "first element", "second element" ]
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "first element, second element")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "first element finally second element")

    def test_3(self):
        x = [ "first element", "second element", "third element" ]
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "first element, second element, third element")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "first element;second element finally third element")

    def test_4(self):
        x = [ "first element", "second element", "third element", "fourth element" ]
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "first element, second element, third element, fourth element")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "first element;second element;third element finally fourth element")

class FormatterCase(unittest.TestCase):
    def test_simple_formatter(self):
        x = [ "one", 2, 2.5, "three" ]
        result = join_list(x)
        print('"{:}"'.format(result))
        self.assertEqual(result, "one, 2, 2.5, three")
        result = join_list(x, ';', ' finally ')
        print('"{:}"'.format(result))
        self.assertEqual(result, "one;2;2.5 finally three")

    def test_string_simple_formatter(self):
        x = [ "one", 2, 2.5, "three" ]
        formatter = "!{0}!"
        result = join_list(x, formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "!one!, !2!, !2.5!, !three!")
        result = join_list(x, ';', ' finally ', formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "!one!;!2!;!2.5! finally !three!")

    def test_string_formatter(self):
        x = [ 16, 2, -42, 621 ]
        formatter = "{:x}"
        result = join_list(x, formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "10, 2, -2a, 26d")
        result = join_list(x, ';', ' finally ', formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "10;2;-2a finally 26d")

    def test_callable_simple_formatter(self):
        x = [ 16, 2, -42, 621 ]
        formatter = hex
        result = join_list(x, formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "0x10, 0x2, -0x2a, 0x26d")
        result = join_list(x, ';', ' finally ', formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "0x10;0x2;-0x2a finally 0x26d")

    def test_callable_lambda_1_formatter(self):
        x = [ 16, 2, -42, 621 ]
        formatter = lambda x: oct(abs(x))
        result = join_list(x, formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "0o20, 0o2, 0o52, 0o1155")
        result = join_list(x, ';', ' finally ', formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "0o20;0o2;0o52 finally 0o1155")

    def test_callable_lambda_2_formatter(self):
        x = [ "first element", "second element", "third element", "fourth element" ]
        formatter = lambda x: "**{0}**".format(x.capitalize())
        result = join_list(x, formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "**First element**, **Second element**, **Third element**, **Fourth element**")
        result = join_list(x, ';', ' finally ', formatter=formatter)
        print('"{:}"'.format(result))
        self.assertEqual(result, "**First element**;**Second element**;**Third element** finally **Fourth element**")

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
