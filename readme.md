Visual Search Server
===============
# (under development)

A simple implementation of Visual Search using TensorFlow, InceptionV3 model and AWS GPU instances.

This codebase implements a simple visual indexing and search system, using features derived from Google's inception 
model trained on the imagenet data. The easist way to use it is to launch following AMI using GPU enabled g2 instances.
It already contains features computed on ~450,000 images (female fashion), the feature computation took 22 hours on 
a spot AWS g2 (single GPU) instance. i.e. ~ 230,000 images / 1 $ . Since I did not use batching, it might be possible to 
get even better performance.
 
The code implements two methods, a server that handles image search, and a simple indexer that extracts pool3 features.
Nearest neighbor search can be performed in an approximate manner using nearpy (faster) or using exact methods (slower). 

![Alpha Screenshot](appcode/static/alpha3.png "Alpha Screenshot")     

 