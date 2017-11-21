import sys
from yaml import load

class Config():
    def __init__(self, defaults=None):
        self.LOGO = 'aha!'

    def from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                try:
                    content = load(f)
                    for k in content:
                        setattr(self, k, content[k])
                except Exception as e:
                    print('json parse error: {}'.format(e))
                    sys.exit(1)
        except Exception as e:
            print('open config file error: {}'.format(e))
            sys.exit(1)

config = Config()
