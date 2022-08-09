# {{0}}  {{*}} {{1}} {{ a | fx }}
# {{}}  -- > {{

import re
from typing import Callable, Dict, Generator, List, Union

Value = Union[str, Callable, List[str]]
Context = Dict[str, Value]


class WrappedValue:
    """The wrapper class for Value.

    Attributes:
        value: An Object the value corresponding to key.
        isFunc: A boolean indicating if as a function or not.
        key: .
    """
    __slots__ = ['value', 'isFunc', 'key']

    def __init__(self, key: str, value: Value) -> None:
        self.key = key
        self.value = value
        self.isFunc: bool = key and key[0] != '&' and callable(value)

    def __str__(self) -> str:
        v = self.value
        if isinstance(v, str):
            return "'{}'".format(v)
        elif isinstance(v, list):
            return str(v)
        return self.key

    def __repr__(self) -> str:
        v=self.value
        if isinstance(self.value,str):
            v = f"'{v}'"
        return f'<{self.__class__.__name__}; key={self.key}, isFunc={self.isFunc}, value={v}>'

    @classmethod
    def getWrapper(cls, ctx: Context):
        def w(k: str):
            k = k.strip()
            if k[0] == '&':
                func_name = k[1:].strip()
                return WrappedValue('&'+func_name, ctx[func_name])
            elif k[0] == "'" and k[-1] == "'":  # 字面量
                flag, ss = 0, []
                for s in k[1:-1]:
                    if flag == 1:
                        if s in ['\\', '|', "'"]:
                            ss.append(s)
                            flag = 0
                        else:
                            raise SyntaxError("An illegal escape character")
                    else:
                        if s == '\\':
                            flag = 1
                            continue
                        if s in ['\\', '|', "'"]:
                            raise SyntaxError("An illegal character {}".format(s))
                        ss.append(s)
                if flag:
                    raise SyntaxError("An illegal escape character")
                return WrappedValue(None, ''.join(ss))
            return WrappedValue(k, ctx[k])
        return w

    pass


__r = re.compile(r'(?<!\\)\|')


def conv(k: str, ctx: Context):
    '''
    "a | func " => [ "a" , func ]
    '''
    w = WrappedValue.getWrapper(ctx)
    return [w(x) for x in __r.split(k)]


def convertor01(text: str, ctx: Context) -> List[Union[str, List[WrappedValue]]]:
    '''
    a=[1,2],b="o",c=func

    "x{{a}}y" => [ 'x' , [[1,2]] ,'y' ]

    "x{{b|c}}y" => [ 'x' , ["o",func] ,'y' ]

    "x{{b}}y" => [ 'x' , ["o"] ,'y' ]
    '''
    res, kk, ss, state = [], [], [], 0
    cnt = 0
    for c in text:
        if state < 2:
            if c == '{':
                kk.append(c)
                state += 1
            else:
                ss.append(('{'*state)+c)
                state, kk = 0, []
        elif state == 2:
            if c == '}' and cnt in [0, 2]:
                state += 1
            elif c == "'":  # 字面量
                if len(kk) > 0 and kk[-1] != "\\":
                    cnt += 1
            if cnt > 2:
                raise SyntaxError('Mismatched quotes')
            elif cnt == 0 and c == '\\':
                raise SyntaxError('An illegal escape character')
            if c == '|' and len(kk) > 0 and kk[-1] != "\\":
                if cnt not in [0, 2]:
                    raise SyntaxError('Mismatched quotes')
                else:
                    cnt = 0
            kk.append(c)
        elif state == 3:
            if c == '}':
                k = ''.join(kk[2:-1]).strip()
                if len(ss) > 0:
                    res.append(''.join(ss))
                    ss = []
                res.append(conv(k, ctx) if k else '{{')
            else:
                ss.extend(kk)
            state, kk = 0, []
        pass
    if cnt not in [0, 2]:
        raise SyntaxError('Mismatched quotes')
    ss.extend(kk)
    # TODO FIX
    if len(ss) > 0:
        res.append(''.join(ss))
    return res


def convertor02(vals: List[WrappedValue]):
    '''
    ['a',upper,[0,1]] => ['A',[0,1]]  => [['A',0],['A',1]]
    '''
    if not isinstance(vals, list):
        raise ValueError(
            'The vals variable is of the wrong type,expect List[WrappedValue] but {}', type(vals))
    st:  List[Union[str, List[str]]] = []
    for v in vals:
        if v.isFunc:
            import inspect
            n = len(inspect.signature(v.value).parameters)
            if n > 0:
                ps = st[-n:]
                st = st[:-n]
                r = v.value(*ps)
            else:
                r = v.value()
            if r:
                st.extend(r)
        else:
            st.append(v.value)
    return convertor03(st)


def convertor03(vals:  List[Union[str, List[str]]], prefix: List[str] = None, i: int = 0) -> Generator[List[str], None, None]:
    '''
    ['A',[0,1]]  => [['A',0],['A',1]]
    '''
    prefix, t = prefix if prefix else [], []
    from inspect import isgenerator
    for ii in range(i, len(vals)):
        x = vals[ii]
        if isgenerator(x):
            x = list(x)
        if isinstance(x, list):
            if len(x) == 1:  # 优化性能
                if len(t) > 0:
                    prefix.append(''.join(t))
                    t = []
                prefix.append(str(x[0]))
            else:
                for xx in x:
                    pp = prefix.copy()
                    if len(t) > 0:
                        pp.append(''.join(t))
                    pp.append(str(xx))
                    yield from convertor03(vals, pp, ii+1)
                return
        else:
            t.append(str(x))
    if len(t) > 0:
        prefix.append(''.join(t))
    yield prefix
