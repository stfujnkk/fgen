import os

from ..utils import open_for_save
from ..config.config import Config
from ..config.node import Node


class Router:
    __slots__ = ['conf']

    def __init__(self, conf: Config) -> None:
        self.conf = conf

    def forward(self):
        base = self.conf.base
        for root, _, fs in os.walk(base):
            for f in fs:
                fullname = os.path.join(root, f)
                for pm in self.conf.pathMappers:
                    uri = os.path.relpath(fullname, start=base)
                    ctx = {}
                    outputs = pm.mapping(uri, ctx)
                    if outputs:
                        for output in outputs:
                            node = Node()
                            node.root = base
                            node.template_path = uri
                            node.output_path = output
                            # 上下文
                            tpl = self.conf.environment.get_template(uri)
                            ctx['template_base'] = base
                            ctx['template_path'] = uri
                            ctx['file_name'] = os.path.basename(''.join(output))
                            ctx['file_path'] = output
                            ctx['match_groups'] = ctx['*']
                            node.data = tpl.render(**ctx)
                            for conv in pm.converters:
                                if conv(node):
                                    continue
                            for conv in self.conf.converters:
                                if conv(node):
                                    continue
                            # 默认输出到文件
                            pth = node.output_path
                            if isinstance(pth, list):
                                pth = ''.join(pth)
                            with open_for_save(os.path.join(self.conf.dest, pth)) as f:
                                f.write(node.data)
                        break
                    pass
                pass
        pass

    pass
