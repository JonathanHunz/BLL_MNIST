#!/usr/bin/env python
import logging
import utils
import json

# Set log level to info
logging.basicConfig(level=logging.INFO)

# Load dataset description file
dataset_description = json.load(open("./dataset.json"))

# Download resource
downloader = utils.Downloader(dataset_description, "../../data/raw")
downloader.download()

# Extract resources
extractor = utils.Extractor(dataset_description, "../../data/raw", "../../data/processed")
extractor.extract()
