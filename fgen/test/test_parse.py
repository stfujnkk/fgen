from ..core import parse
import unittest
from deepdiff import DeepDiff


class Test_convertor01(unittest.TestCase):
    def test_convertor01_01(self):
        self.assertEqual(
            DeepDiff(parse.convertor01("{{}}", {}), [ "{{" ]), {})

    def test_convertor01_02(self):
        self.assertEqual(DeepDiff(parse.convertor01("{{'a'}}", {}), [ [parse.WrappedValue(None, "a")]]), {})

    def test_convertor01_03(self):
        self.assertEqual(DeepDiff(parse.convertor01("{{'}}{{'}}", {}), [ [parse.WrappedValue(None, "}}{{")]]), {})

    def test_convertor01_04(self):
        ss = parse.WrappedValue(None, 'O0o')
        func = parse.WrappedValue("lower", str.lower)
        self.assertEqual(DeepDiff(parse.convertor01("{{ 'O0o' | lower }}", {
                         "lower": str.lower}), [  [ss, func] ]), {})

    def test_convertor01_05(self):
        a = [0, 1]
        wa = parse.WrappedValue("a", a)
        d = {"a": a}
        self.assertEqual(DeepDiff(parse.convertor01(
            "x{{ a }}y", d), ["x", [wa], "y"]), {})

    def test_convertor01_06(self):
        a = "kk"
        wa = parse.WrappedValue("a", a)
        d = {"a": a}
        self.assertEqual(DeepDiff(parse.convertor01(
            "x{{ a }}y", d), ["x", [wa], "y"]), {})

    def test_convertor01_07(self):
        a = "kk"
        wa = parse.WrappedValue("a", a)
        d = {"a": a}
        self.assertEqual(DeepDiff(parse.convertor01(
            "x{{ a }}yascsa", d), ["x", [wa], "yascsa"]), {})

    def test_convertor01_08(self):
        a = "kk"
        f = str.lower
        wa = parse.WrappedValue("a", a)
        wf = parse.WrappedValue("lower", f)
        d = {"a": a, "arr": [1, 2], "lower": f}
        self.assertEqual(DeepDiff(parse.convertor01("x{{ a }}yasc{{ a | lower }}sa", d), [
                         "x", [wa], "yasc", [wa, wf], "sa"]), {})

    def test_convertor01_09(self):
        self.assertEqual(DeepDiff(parse.convertor01("x{{ 'Aa' | 'Ggx\\'' }}sa", {}), ["x", [
            parse.WrappedValue(None, "Aa"),
            parse.WrappedValue(None, "Ggx'"),
        ], "sa"]), {})

    def test_convertor01_10(self):
        v = "你好ok?？"
        self.assertEqual(DeepDiff(parse.convertor01("x{{ 0 }}sa", {"0": v}), [
                         "x", [parse.WrappedValue("0", v)], "sa"]), {})

    def test_convertor01_11(self):
        f = str.lower
        self.assertEqual(DeepDiff(parse.convertor01("x{{ &low }}sa", {"low": f}), [
                         "x", [parse.WrappedValue("&low", f)], "sa"]), {})


class Test_convertor02(unittest.TestCase):
    def test_convertor02_01(self):
        self.assertRaises(ValueError, parse.convertor02, 'abc')

    def test_convertor02_02(self):
        d = {
            "ka": "a",
            "upper": str.upper,
            "arr": [0, 1],
        }
        wvs = [parse.WrappedValue(k, v) for k, v in d.items()]
        self.assertEqual(
            DeepDiff([x for x in parse.convertor02(wvs)], [['A', '0'], ['A', '1']]), {})
        self.assertEqual(
            DeepDiff([x for x in parse.convertor02(wvs[:-1])], [['A']]), {})
        self.assertEqual(
            DeepDiff([x for x in parse.convertor02(wvs[0:1])], [['a']]), {})
        wvs.append(wvs[-1])
        self.assertEqual(DeepDiff([x for x in parse.convertor02(wvs)], [
            ['A', '0', '0'],
            ['A', '0', '1'],
            ['A', '1', '0'],
            ['A', '1', '1'],
        ]), {})

    def test_convertor02_03(self):
        wvs = [parse.WrappedValue("ka", "a"), parse.WrappedValue(
            "&upper", str.upper), ]
        self.assertEqual(DeepDiff(list(parse.convertor02(wvs)), [
                         ["a<method 'upper' of 'str' objects>"]]), {})

    def test_convertor02_04(self):
        def myUpper(x: str):
            return x.upper()
        wvs = [parse.WrappedValue("ka", "a"),
               parse.WrappedValue("myUpper", myUpper), ]
        self.assertEqual(
            DeepDiff([x for x in parse.convertor02(wvs)], [['A']]), {})

    def test_convertor02_05(self):
        def mySquare(x: int): return x*x
        def fmap(xs, f): return [f(x) for x in xs]
        wvs = [parse.WrappedValue("arr", [1, 3]), parse.WrappedValue(
            "&mySquare", mySquare), parse.WrappedValue("fmap", fmap)]
        # convertor03 会将结果合并
        self.assertEqual(
            DeepDiff([x for x in parse.convertor02(wvs)], [['19']]), {})

    pass


class Test_convertor03(unittest.TestCase):
    def test_convertor03_01(self):
        self.assertEqual(
            DeepDiff(list(parse.convertor03(['a', 'b'])), [['ab']]), {})

    def test_convertor03_02(self):
        self.assertEqual(DeepDiff(list(parse.convertor03(['a', [0, 1]])), [
                         ['a', '0'], ['a', '1']]), {})

    def test_convertor03_03(self):
        t1 = list(parse.convertor03(['a', [0, 1], ['X', 'Y']]))
        t2 = [['a', '0', 'X'], ['a', '0', 'Y'],
              ['a', '1', 'X'], ['a', '1', 'Y']]
        self.assertEqual(DeepDiff(t1, t2), {})

    def test_convertor03_04(self):
        t1 = list(parse.convertor03(['a', [0, 1], 'F', '-', ['X', 'Y']]))
        t2 = [['a', '0', 'F-', 'X'], ['a', '0', 'F-', 'Y'],
              ['a', '1', 'F-', 'X'], ['a', '1', 'F-', 'Y']]
        self.assertEqual(DeepDiff(t1, t2), {})

    def test_convertor03_05(self):
        t1 = list(parse.convertor03([['a'], ['0'], ['1']]))
        t2 = [['a', '0', '1']]
        self.assertEqual(DeepDiff(t1, t2), {})

    def test_convertor03_06(self):
        t1 = list(parse.convertor03([['a'], '-', 'x', ['1'], 'G', 'h']))
        t2 = [['a', '-x', '1', 'Gh']]
        self.assertEqual(DeepDiff(t1, t2), {})

    def test_convertor03_07(self):
        g = (x for x in range(3))
        t1 = list(parse.convertor03(['G', '-', g]))
        t2 = [['G-', '0'], ['G-', '1'], ['G-', '2']]
        self.assertEqual(DeepDiff(t1, t2), {})

    pass
