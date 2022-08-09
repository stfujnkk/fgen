from ..config.pathMapper import PathMapper

import unittest
from deepdiff import DeepDiff


class Test_pathMapper(unittest.TestCase):
    def test_pathMapper_01(self):
        pm = PathMapper(r'(user)-(\d+)', '/{{1}}{{2}}')
        self.assertEqual(pm.mapping('x', {}), None)
        self.assertEqual(pm.mapping('user-a', {}), None)
        self.assertEqual(pm.mapping('xuser-01', {}), None)

    def test_pathMapper_02(self):
        pm = PathMapper(r'(user)-(\d+)', '/{{1}}')
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [[ "/","user" ]] ),{})
        pm = PathMapper(r'(user)-(\d+)', '/{{0}}')
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [[ "/","user-01" ]] ),{})
        pm = PathMapper(r'(user)-(\d+)', '/{{*}}')
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['/', 'user'], ['/', '01']]  ),{})
    
    def test_pathMapper_03(self):
        pm = PathMapper(r'(user)-(\d+)', "{{ '\\\\|'  }}")
        self.assertRaises(SyntaxError,pm.mapping,'user-01')
        pm = PathMapper(r'(user)-(\d+)', "{{ '\\\\\\|' }}")
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['\\|']]),{})
        pm = PathMapper(r'(user)-(\d+)', "{{ '\\\\\\'' }}")
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [["\\'"]]),{})
        pm = PathMapper(r'(user)-(\d+)', "{{ '\\' }}")
        self.assertRaises(SyntaxError,pm.mapping,'user-01')

    def test_pathMapper_04(self):
        f = str.capitalize
        pm = PathMapper(r'(user)-(\d+)', '/{{1|f}}{{2}}',define={"f":f})
        self.assertEqual(DeepDiff(list(pm.mapping('user-01', { "f":str.upper})), [ [ "/","User","01" ] ]),{})

    def test_pathMapper_05(self):
        f = str.capitalize
        pm = PathMapper(r'(user)-(\d+)', '/{{1|f}}{{2}}',define={"f":f})
        self.assertEqual(DeepDiff(list(pm.mapping('user-01', { "f":str.upper})), [ [ "/","User","01" ] ]),{})

    def test_pathMapper_06(self):
        pm = PathMapper(r'(user)-(\d+)', '/{{1}}{{id}}',define= {"id":[1,2,3]})
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [ [ "/","user","1" ],[ "/","user","2" ],[ "/","user","3" ] ]),{})

    def test_pathMapper_07(self):
        pm = PathMapper(r'(user)-(\d+)', '{{id}}{{id}}',define= {"id":[0,1]})
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['0','0'],['0','1'],['1','0'],['1','1']]),{})

    def test_pathMapper_08(self):
        pm = PathMapper(r'(user)-(\d+)', '{{id}}{{ww}}',define= {"id":[0,1]})
        self.assertRaises(KeyError,pm.mapping,'user-01')

    def test_pathMapper_09(self):
        rgx=r'(?P<user>\w+)@(?P<website>\w+)\.(?P<extension>\w+)'
        pm = PathMapper(rgx, 'Hello {{user}}')
        self.assertEqual(DeepDiff(list(pm.mapping('lyf@hackerrank.com')), [['Hello ','lyf']]),{})

    def test_pathMapper_10(self):
        pm = PathMapper(r'(user)-(\d+)', '{{0}}',define= {"0":"xxx"})
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['user-01']]),{})

    def test_pathMapper_11(self):
        pm = PathMapper(r'(user)-(\d+)', '{{1|2}}')
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['user01']]),{})

    def test_pathMapper_12(self):
        pm = PathMapper(r'(user)-(\d+)', "{{1|'???'}}")
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['user???']]),{})
        pm = PathMapper(r'(user)-(\d+)', "{{1|'{{'}}")
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['user{{']]),{})

    def test_pathMapper_13(self):
        pm = PathMapper(r'(user)-(\d+)', "{{1|'")
        self.assertRaises(SyntaxError,pm.mapping,'user-01')
        pm = PathMapper(r'(user)-(\d+)', "{{1|'\\'")
        self.assertRaises(SyntaxError,pm.mapping,'user-01')
        pm = PathMapper(r'(user)-(\d+)', "{{1|'\\''+'a'")
        self.assertRaises(SyntaxError,pm.mapping,'user-01')
        pm = PathMapper(r'(user)-(\d+)', "{{1|'gg'+'a'")
        self.assertRaises(SyntaxError,pm.mapping,'user-01')
        pm = PathMapper(r'(user)-(\d+)', "{{1|'{{\\'g' |'\\''}}")
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [["user{{'g'"]]),{})
        pm = PathMapper(r'(user)-(\d+)', "{{1| '\"'  ")
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['{{1| \'"\'  ']]),{})
        pm = PathMapper(r'(user)-(\d+)', "{{1| '\"'  }}")
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['user"']]),{})

    def test_pathMapper_14(self):
        pm = PathMapper(r'(user)-(\d+)', "{{1| '\\|'  }}")
        self.assertEqual(DeepDiff(list(pm.mapping('user-01')), [['user|']]),{})
        pm = PathMapper(r'(user)-(\d+)', "{{1| \\| }}")
        self.assertRaises(SyntaxError,pm.mapping,'user-01')
    
    
    pass
