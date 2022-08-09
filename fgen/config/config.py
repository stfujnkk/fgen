from typing import Any, Dict, List

from fgen.config.extractor import get_extractor_actuator

from .pathMapper import PathMapper
from .converter import Converter, get_converter_factory
from ..utils import get_environment, read_json, load_plugins, simple_parse, env

'''
{
    "imports": [],
    "extractors": [{
        "provider": "pa.fx",
        "param": {}
    }],
    "converters": [{
        "id": "pa.fx",
        "param": {}
    }],
    "define": {},
    "base": "a.jinja2",
    "dest": "{{b}}.xml",
    "pathMappers": [
        {
            "pattern": "a.jinja2",
            "dest": "{{b}}.xml",
            "define": {},
            "converters": [],
            "extractors": [],
            "imports": []
        }
    ]
}

'''


class Config:
    __slots__ = ['base', 'dest', 'define', 'extractors',
                 'converters', 'pathMappers', 'environment']
    plugins = load_plugins()

    def __init__(self, json_data: Dict[str, Any], isRoot=True, plug_base: str = None, template_base: str = None,) -> None:
        if plug_base:
            Config.plugins = load_plugins(plug_base)
        self.pathMappers: List[PathMapper] = json_data.get('pathMappers', [])
        self.define: Dict[str, Any] = json_data.get('define', {})
        self.converters: List[Converter] = json_data.get('converters', [])
        self.extractors = json_data.get('extractors', [])

        self.__import_config(json_data.get('imports', []))

        if isRoot:
            self.base: str = simple_parse(json_data['base'], self.define)
            self.dest: str = simple_parse(json_data['dest'], self.define)

            self.environment = get_environment(template_base or self.base)
            self.environment.globals.update(self.define)
            self.environment.globals['plugins'] = self.plugins

            actuator = get_extractor_actuator(self.plugins, self.environment)
            for extractor in self.extractors:
                actuator(extractor)
            factory = get_converter_factory(self.plugins)
            self.converters = [factory(x) for x in self.converters]

            def conv2pathmapper(conf: Dict[str, Any]):
                conf['plugins'] = self.plugins
                return PathMapper(**conf)

            self.pathMappers = [conv2pathmapper(x) for x in self.pathMappers]

    def __import_config(self, paths: List[str]):
        for pth in paths:
            data = read_json(pth)
            self.merge(Config(data, False))

    def merge(self, conf):
        self.converters.extend(conf.converters)
        self.extractors.extend(conf.extractors)
        d = conf.define.copy()
        d.update(self.define)
        self.define = d
        self.pathMappers.extend(conf.pathMappers)

    @classmethod
    def get_config_base(cls, base: str):
        import os
        os.chdir(base)
        return Config(
            json_data=read_json(os.path.join(base, 'config.json')),
            plug_base=os.path.join(base, 'plugins'),
            template_base=os.path.join(base, 'templates')
        )

    pass
