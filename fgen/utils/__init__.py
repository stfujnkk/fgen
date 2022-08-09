import json
from jinja2 import Template
from operator import attrgetter
import types
from typing import Any, Callable, Dict

from .env import default_templates_dir, plugins_dir
import os
import sys

# from ..config.config import Config

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
class PlugNamespace:
    def get_attr(self, attr: str)->Any: ...
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def open_for_read(file_path: str):
    return open(file_path, 'r', encoding='utf8')


def read_json(file_path: str):
    with open_for_read(file_path) as f:
        conf = json.load(f)
    return conf


def open_for_save(file_path: str):
    return open(file_path, "w", encoding='utf8')


def save_json(file_path: str, data):
    with open_for_read(file_path) as f:
        json.dump(data, f, ensure_ascii=False)


def load_plugins(base:str=None) -> PlugNamespace:
    base = base or plugins_dir
    from importlib import import_module
    if not os.path.exists(base):
        os.makedirs(base)
    sys.path.append(base)
    plugins = types.SimpleNamespace()
    for plugin_name in os.listdir(base):
        is_file = os.path.isfile(os.path.join(base, plugin_name))
        if is_file and plugin_name.endswith('.py'):
            n = plugin_name[:-3]
            setattr(plugins, n, import_module(n))
        elif not is_file:
            setattr(plugins, plugin_name, import_module(plugin_name))
    sys.path.remove(base)
    setattr(plugins, 'get_attr', get_getter(plugins))
    return plugins


def get_environment(templates_dir:str=None):
    from jinja2 import Environment, FileSystemLoader
    environment = Environment(loader=FileSystemLoader(searchpath = templates_dir or default_templates_dir))
    return environment

def get_getter(x) -> Callable[[str], Any]:
    return lambda attr: attrgetter(attr)(x)

def simple_parse(s:str,ctx:Dict[str,Any])->str:
    return Template(s).render(ctx)

