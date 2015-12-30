A simple implementation of Visual Search using TensorFlow, Inception version 3 models and AWS GPU instances  (under development)
==================

This codebase implements a simple visual indexing and search system, using features derived from Google's inception 
model training on the imagenet data. The easist way to use this codebase is to launch following AMI using GPU enabled g2 instances.
 
The code implements two methods, a server that handles image search, and a simple indexer that extracts pool3 features.














Please take a look at notebook_index.ipynb to see examples of results from Nearest Neighbor search on Inception Pool 3 layer features.
 