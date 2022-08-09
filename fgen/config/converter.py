from typing import Any, Callable, Dict

from ..utils import PlugNamespace

from .node import Node

Converter = Callable[[Node], bool]

def get_converter_factory(plugins:PlugNamespace):
    def __converter_factory(conf:Dict[str,Any])->Converter:
        param = conf.get('param',{})
        f = plugins.get_attr(conf['provider'])
        return lambda node:f(node,**param)
    return __converter_factory
