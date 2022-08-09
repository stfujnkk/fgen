import sys
from .config.config import Config
from .core.router import Router
from .utils import read_json,env

def main():
    if len(sys.argv) == 2:
        conf = Config(read_json(sys.argv[1]))
    else:
        conf = Config(read_json(env.conf_path))
    Router(conf).forward()

if __name__ == '__main__':
    main()
