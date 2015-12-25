import os,time,random
from collections import defaultdict
import gzip
import numpy as np
import cv2
from cv2 import cv
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

    def get_image(self,key,bucket_name):
        im_str = s3_client.get_object(Bucket=bucket_name,Key='{}'.format(key))['Body'].read()
        nparr = np.fromstring(im_str,np.uint8)
        return cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)

    def get_images(self,bucket_name):
        for model in self.models:
            for k in self.models[model]:
                yield model,k,self.get_image(k,bucket_name)


if __name__ == "__main__":
    d = Dataset()
    print len(d.models)