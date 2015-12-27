import time,glob,re,sys,logging,os
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/worker.log',
                    filemode='a')

BATCH_SIZE = 1000
AWS = sys.platform != 'darwin'

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




with gfile.FastGFile('network.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def get_batch():
    path = "/mnt/dataset/*" if AWS else "dataset*/*.jpg"
    image_data = {}
    logging.info("starting with path {}".format(path))
    for i,fname in enumerate(glob.glob(path)):
        try:
            image_data[fname] = gfile.FastGFile(fname, 'rb').read()
        except:
            logging.info("failed to load {}".format(fname))
            pass
        if i % BATCH_SIZE == 0:
            logging.info("Loaded {}".format(i))
            yield image_data
            image_data = {}
    yield image_data
    logging.info("Finished {}".format(i))



if __name__ == '__main__':
    import marshal
    count = 0
    start = time.time()
    with tf.Session() as sess:
        node_lookup = NodeLookup()
        pool3 = sess.graph.get_tensor_by_name('pool_3:0')
        for image_data in get_batch():
            logging.info("starting feature extraction batch {}".format(len(image_data)))
            start = time.time()
            features,files = [],[]
            count += 1
            for fname,data in image_data.iteritems():
                try:
                    pool3_features = sess.run(pool3,{'DecodeJpeg/contents:0': data})
                    features.append(np.squeeze(pool3_features))
                    files.append(fname)
                except:
                    print "Error",fname.split('/')[-1]
                    pass
            logging.info(str(time.time()-start))
            feat_fname = "{}.feats_pool3.400k.npy".format(count)
            files_fname = "{}.400k.files".format(count)
            with open(feat_fname,'w') as feats:
                np.save(feats,np.array(features))
            with open(files_fname,'w') as filelist:
                filelist.write("\n".join(files))
            if AWS:
                os.system('aws s3 mv {} s3://aub3visualsearch/ --region "us-east-1"'.format(feat_fname))
                os.system('aws s3 mv {} s3://aub3visualsearch/ --region "us-east-1"'.format(files_fname))
                logging.info("uploaded {}".format(feat_fname))
