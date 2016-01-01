__author__ = 'aub3'
import os,sys
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'appcode/vendor'))
vendor_dir = os.path.join(os.path.dirname(__file__), 'appcode/vendor')
try:
    import google
    google.__path__.append(os.path.join(vendor_dir, 'google'))
except ImportError:
    pass
from appcode import app
from settings import AWS
if __name__ == '__main__':
    if AWS:
        app.run(host="0.0.0.0",port=9000)
    else:
        app.run(port=9992,debug=True)