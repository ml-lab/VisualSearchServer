import sys,time,os,glob,logging
sys.path.append('/home/ubuntu/crfasrnn/caffe-crfrnn/python')
import caffe
import numpy as np
from settings import pallete
from PIL import Image as PILImage


def process(input_image,net):
    """

    :param image:
    :param net:
    :return:
    """
    width,height = input_image.shape[0],input_image.shape[1]
    image = PILImage.fromarray(np.uint8(input_image))
    image = np.array(image)
    mean_vec = np.array([103.939, 116.779, 123.68], dtype=np.float32)
    reshaped_mean_vec = mean_vec.reshape(1, 1, 3)
    im = image[:,:,::-1] # Rearrange channels to form BGR
    im = im - reshaped_mean_vec # Subtract mean
    cur_h, cur_w, cur_c = im.shape # Pad as necessary
    pad_h,pad_w = 500 - cur_h, 500 - cur_w
    im = np.pad(im, pad_width=((0, pad_h), (0, pad_w), (0, 0)), mode = 'constant', constant_values = 0)
    segmentation = net.predict([im]) # Get predictions
    return segmentation[0:cur_h, 0:cur_w]

if __name__ == '__main__':
    net = caffe.Segmenter('/home/ubuntu/crfasrnn/python-scripts/TVG_CRFRNN_COCO_VOC.prototxt', '/home/ubuntu/crfasrnn/python-scripts/TVG_CRFRNN_COCO_VOC.caffemodel')
    for fname in glob.glob("/home/ubuntu/crfasrnn/python-scripts/data/*.jpg"):
        start = time.time()
        input_image = 255 * caffe.io.load_image(fname)
        segments = process(input_image,net)
        print "{}\t{}".format(fname,time.time()-start)
        output_im = PILImage.fromarray(segments)
        output_im.putpalette(pallete)
        output_im.save("{}.png".format(fname.split('/')[1].split('.')[0]))

"""
input_image = 255 * caffe.io.load_image(fname[76])
segments = process(input_image,net)
blob = 'coarse'
for k in range(net.blobs[blob].data.shape[1]):
    data = net.blobs[blob].data[0,k,:,:]
    plt.figure()
    plt.title("{} {}".format(k,data.max()))
    plt.imshow(data,cmap='hot')
"""
