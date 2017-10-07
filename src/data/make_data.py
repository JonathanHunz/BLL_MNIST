#!/usr/bin/env python
import logging
import utils

# Set log level to info
logging.basicConfig(level=logging.INFO)
downloader = utils.Downloader("./data/raw")
# Training data
downloader.add_to_queue("train_data", "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz", "gz")
# Training labels
downloader.add_to_queue("train_labels", "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz", "gz")

# Download resources in queue
downloader.download()