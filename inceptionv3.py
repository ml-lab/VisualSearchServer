import re
import numpy as np
import tensorflow as tf
import time,glob
from tensorflow.python.platform import gfile


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


if __name__ == '__main__':
    image_data = []
    for i,fname in enumerate(glob.glob("dataset*/*.jpg")):
        image_data.append(gfile.FastGFile(fname, 'rb').read())
        if i == 100:
            break
    print "{} Images loaded".format(len(image_data))
    with tf.Session() as sess:
        node_lookup = NodeLookup()
        for data in image_data:
            start = time.time()
            pool3 = sess.graph.get_tensor_by_name('pool_3:0')
            pool3_features = sess.run(pool3,{'DecodeJpeg/contents:0': data})
            pool3_features = np.squeeze(pool3_features)
            print pool3_features.shape
            print time.time()-start
            # top_k = predictions.argsort()[-5:][::-1]
            # for node_id in top_k:
            #     human_string = node_lookup.id_to_string(node_id)
            #     score = predictions[node_id]
            #     print('%s (score = %.5f)' % (human_string, score))
