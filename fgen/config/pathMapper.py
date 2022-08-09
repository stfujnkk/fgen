from typing import Any, Dict

import re
from ..core import parse
'''
{
    "id":"xx",
    "pattern": "a.jinja2",
    "dest": "{{b}}.xml",
    "define": {},
    "converters": [],
}
'''
from .converter import get_converter_factory

class PathMapper:
    __slots__ = ['id', 'pattern', 'dest', 'define', 'converters', '__re']

    def __init__(self, pattern: str, dest: str, **kwargs) -> None:
        self.id = kwargs.get('id', f'PathMapper: {pattern}=>{dest}')
        self.pattern = pattern
        self.dest = dest
        self.define: Dict[str, Any] = kwargs.get('define', {})
        converters = kwargs.get('converters', [])
        if len(converters) > 0: # 兼容测试
            conv = get_converter_factory(kwargs['plugins'])
        self.converters=[ conv(x) for x in converters ]
        self.__re = re.compile(self.pattern)
        pass

    def mapping(self, text: str, ctx: Dict[str, str] = None):
        if r := self.__re.match(text):
            d = ctx if ctx != None else {}
            d.update(self.define)
            d['0'] = r.group()
            d['*'] = gs = list(r.groups())
            for i in range(len(gs)):
                d[str(i+1)] = gs[i]
            d.update(r.groupdict())
            # {{0}}  {{*}} {{1}} {{ a | fx }}
            xs = parse.convertor01(self.dest, ctx=d)
            xs = [x if isinstance(x, str) else parse.convertor02(x) for x in xs]
            xs = [x if isinstance(x, str) else [''.join(xx) for xx in x] for x in xs]
            return parse.convertor03(xs)
        else:
            return None
    pass
