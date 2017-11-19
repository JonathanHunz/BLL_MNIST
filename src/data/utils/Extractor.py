import os
import logging

import tensorflow as tf
import numpy as np

from .BinaryReader import BinaryReader


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


class Extractor:
    """Extracts data from data-sources and writes them to a .tfrecords file

    Attributes:
        dataset (dictionary): Dataset specification in form of a dictionary
        input_dir (string): Path of the directory in which the input files can be found
        output_dir (string): Path of the directory in which the .tfrecords file will be generated in
    """

    def __init__(self, dataset, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.dataset = dataset

    def extract(self):
        """Generates features from a given dataset specification and input files and writen the to a .tfrecords file"""

        # Create output directory if not existent
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
            logging.debug("Created data directory (%s)", self.output_dir)

        output_filename = self.dataset["name"] + ".tfrecords"
        output_path = os.path.join(self.output_dir, output_filename)

        logging.info("Extracting data")

        # Create file readers for all features
        feature_readers = {}
        for feature in self.dataset["features"]:
            example_size = np.prod(feature["shape"])
            source_path = os.path.join(self.input_dir, feature["source"])

            reader = BinaryReader(source_path, self.dataset["element_count"], example_size, feature["offset"])

            feature_readers[feature["name"]] = reader

        # Initialize TFRecord writer
        writer = tf.python_io.TFRecordWriter(output_path)

        for _ in range(self.dataset["element_count"]):

            feature_list = {}
            for feature in self.dataset["features"]:

                reader = feature_readers[feature["name"]]

                # Read next element
                raw_data = np.frombuffer(reader.next(), dtype=np.uint8)

                if feature["type"] == "byte":
                    raw_data = raw_data.astype(np.float32)
                    raw_data.resize(feature["shape"])
                    feature_list[feature["name"]] = _bytes_feature(raw_data.tostring())

                elif feature["type"] == "int":
                    raw_data = raw_data.astype(np.int64)
                    raw_data.resize(feature["shape"])
                    feature_list[feature["name"]] = _int64_feature(int(raw_data))

            # Create example
            example = tf.train.Example(features=tf.train.Features(feature=feature_list))
            # Write example to TFRecord
            writer.write(example.SerializeToString())

        writer.close()
