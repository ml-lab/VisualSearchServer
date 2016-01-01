import time,glob,re,sys,logging,os
import numpy as np
import tensorflow as tf
from scipy import spatial
from settings import AWS
from tensorflow.python.platform import gfile
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/worker.log',
                    filemode='a')

BATCH_SIZE = 1000
from settings import AWS


class NodeLookup(object):
    def __init__(self):
        label_lookup_path = 'data/imagenet_2012_challenge_label_map_proto.pbtxt'
        uid_lookup_path = 'data/imagenet_synset_to_human_label_map.txt'
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

    def load(self, label_lookup_path, uid_lookup_path):
        proto_as_ascii_lines = gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]
            human_string = parsed_items[2]
            uid_to_human[uid] = human_string
        node_id_to_uid = {}
        proto_as_ascii = gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: %s', val)
            name = uid_to_human[val]
            node_id_to_name[key] = name
        return node_id_to_name

    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]


def load_network(png=False):
    with gfile.FastGFile('data/network.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        if png:
            png_data = tf.placeholder(tf.string, shape=[])
            decoded_png = tf.image.decode_png(png_data, channels=3)
            _ = tf.import_graph_def(graph_def, name='',input_map={'DecodeJpeg': decoded_png})
            return png_data
        else:
            _ = tf.import_graph_def(graph_def, name='')

def load_index():
    index,files,findex = [],{},0
    index_path = "/mnt/index/*.npy" if AWS else "index/3*.npy"
    for fname in glob.glob(index_path):
        index.append(np.load(fname))
        for f in file(fname.replace(".feats_pool3.npy",".files")):
            files[findex] = f.strip()
            findex += 1
        print fname
    index = np.concatenate(index)
    return index,files

def nearest(query_vector,index,files):
    query_vector= query_vector[np.newaxis,:]
    temp = []
    dist = []
    print "started"
    for k in xrange(index.shape[0]):
        temp.append(index[k])
        if (k+1) % 50000 == 0:
            temp = np.transpose(np.dstack(temp)[0])
            print k+1
            dist.append(spatial.distance.cdist(query_vector,temp))
            temp = []
    if temp:
        temp = np.transpose(np.dstack(temp)[0])
        print k+1
        dist.append(spatial.distance.cdist(query_vector,temp))
    dist = np.hstack(dist)
    ranked = np.squeeze(dist.argsort())
    return [files[k] for i,k in enumerate(ranked[:5])]


def get_batch():
    path = "dataset/*" if AWS else "data/test/*.jpg"
    image_data = {}
    logging.info("starting with path {}".format(path))
    for i,fname in enumerate(glob.glob(path)):
        try:
            image_data[fname] = gfile.FastGFile(fname, 'rb').read()
        except:
            logging.info("failed to load {}".format(fname))
            pass
        if i % BATCH_SIZE == 0:
            logging.info("Loaded {}, with {} images".format(i,len(image_data)))
            yield image_data
            image_data = {}
    yield image_data


def store_index(features,files,count):
    feat_fname = "{}.feats_pool3.npy".format(count)
    files_fname = "{}.files".format(count)
    with open(feat_fname,'w') as feats:
        np.save(feats,np.array(features))
    with open(files_fname,'w') as filelist:
        filelist.write("\n".join(files))
    if AWS:
        os.system('aws s3 mv {} s3://aub3visualsearch/450k/ --region "us-east-1"'.format(feat_fname))
        os.system('aws s3 mv {} s3://aub3visualsearch/450k/ --region "us-east-1"'.format(files_fname))
        logging.info("uploaded {}".format(feat_fname))

def extract_features(image_data,sess):
    pool3 = sess.graph.get_tensor_by_name('pool_3:0')
    start = time.time()
    features = []
    files = []
    for fname,data in image_data.iteritems():
        try:
            pool3_features = sess.run(pool3,{'DecodeJpeg/contents:0': data})
            features.append(np.squeeze(pool3_features))
        except:
            logging.error("error while processing fname {}".format(fname))
    logging.info(str(time.time()-start))
    return features,files


def download(filename):
    try:
        os.mkdir("appcode/static/examples")
    except:
        pass
    if AWS:
        os.system("cp dataset/{} examples/{}".format(filename.split("/")[-1],filename.split("/")[-1]))
    else:
        os.system("aws s3 cp s3://aub3data/dataset/{} appcode/static/examples/{}".format(filename.split("/")[-1],filename.split("/")[-1]))

if __name__ == '__main__':
    load_network()
    count = 0
    with tf.Session() as sess:
        node_lookup = NodeLookup()
        for image_data in get_batch():
            logging.info("starting feature extraction batch {}".format(len(image_data)))
            count += 1
            features,files = extract_features(image_data,sess)
