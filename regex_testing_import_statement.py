import unittest
from re import match

rs = r"^\s*(?<!from .)import ((?!\d)\w+)"
rsd = rf"{rs}|^__import__\([\'\"](.+)[\'\"]\)"


def regex(string):
    return match(rs, string)


class MyTestCase(unittest.TestCase):
    def test_easy(self):
        self.assertRegex("import module", rs, "Normal")
        self.assertRegex("    import module", rs, "Normal space indented")
        self.assertRegex("\timport module", rs, "Normal tab indented")
        self.assertRegex("import module as t", rs, "Normal with name change")
        self.assertRegex("import d3", rs, "Module name has number")
        self.assertNotRegex("import 3d", rs, "Module name starting with a number")

    def test_medium(self):
        self.assertRegex("import module name", rs, "Module name has space")
        self.assertNotRegex("from module import *", rs, "From import everything")
        self.assertNotRegex("from module import Thing, Thing2", rs, "From import functions")
        self.assertNotRegex("from module import Thing as t", rs, "From import function with different name")

    def test_hard(self):
        temp = regex("import module_package.idk").group(1)
        self.assertEqual(temp, "module_package", "Module name excluding packages")
        self.assertNotRegex("from module import (Thing1, Thing2)", rs, "From imports in tuple")
        self.assertNotRegex("from module import (\n    Thing1, \n    Thing2\n)", rs, "From imports in tuple and on "
                                                                                     "new lines")
        self.assertRegex("import module; import module2", rs, "Multi-line import statement")
        self.assertRegex("__import__(\"module\").functionName", rs, "__import__")


if __name__ == '__main__':
    unittest.main()
