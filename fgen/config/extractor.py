from typing import Any, Callable, Dict
from ..utils import PlugNamespace

Extractor = Callable[[Dict[str, Any], Dict[str, Any]], bool]


def get_extractor_actuator(plugins:PlugNamespace,env):
    def __extractor_actuator(conf:Dict[str,Any]):
        param = conf.get('param',{})
        f = plugins.get_attr(conf['provider'])
        return f(env,**param)
    return __extractor_actuator
