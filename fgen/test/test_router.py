from ..utils import open_for_read, open_for_save
from ..core.router import Router
from ..config.config import Config

import unittest
from deepdiff import DeepDiff
import os
import sys


class Test_router(unittest.TestCase):
    def setUp(self):
        self.test_root = os.path.dirname(os.path.abspath(__file__))
        self.test_root = os.path.join(self.test_root, 'test_env')
        self.conf = Config.get_config_base(self.test_root)
        self.router = Router(self.conf)
        self.template_dir = os.path.join(self.test_root, 'templates')
        self.plugins_dir = os.path.join(self.test_root,  'plugins')
        self.define = self.router.conf.environment.globals

    def test_router_01(self):
        self.assertEqual(self.define.get('a'), 'JJ')
        self.assertEqual(self.define.get('b'), 0)
        self.assertEqual(self.define.get('c'), None)

    def test_router_02(self):
        self.assertEqual(self.define.get('Fsac'), 'gg')
        self.assertEqual(self.define.get('xx'), 's')
        
    def test_router_03(self):
        try:
            os.remove(os.path.join(self.template_dir,'a.txt.jinja2'))
            os.remove(os.path.join(self.test_root,self.conf.dest,'a.txt'))
        except:
            pass
        with open_for_save(os.path.join(self.template_dir,'a.txt.jinja2')) as f:
            f.write('{{file_name}},{{match_groups[0]}},{{xx}},{{plugins.pa.fy()}}')
        self.router.forward()
        with open_for_read(os.path.join(self.test_root,self.conf.dest,'a.txt')) as f:
            self.assertEqual(f.read(), 'a.txt,a.txt,7,YYY')

    pass
