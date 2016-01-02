__author__ = 'aub3'
import os,sys
sys.path.insert(1, os.path.join(os.path.abspath('.'), ''))
from appcode import app
from settings import AWS
if __name__ == '__main__':
    if AWS:
        app.run(host="0.0.0.0",port=9000)
    else:
        app.run(port=9992,debug=True)