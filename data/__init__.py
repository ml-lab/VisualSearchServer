import os,time,random
from collections import defaultdict
import gzip
import numpy as np
from boto3.session import Session
session = Session()
s3 = session.resource('s3')
s3_client = session.client('s3')


class Dataset(object):
    def __init__(self):
        self.models = defaultdict(dict)
        for line in gzip.GzipFile(os.path.join(os.path.dirname(__file__),"data.txt.gz")):
            try:
                date,time,size,key = line.strip().split()
                _,name,fname = key.split('/')
                self.models[name][key] = {'size':int(size)}
            except:
                print line

    def sorted(self):
        for k,v in sorted([ (len(v),k) for k,v in self.models.iteritems()],reverse=True):
            yield k,v