import os
import logging
import urllib.request


class Downloader:
    def __init__(self, dataset, output_dir):
        self.dataset = dataset
        self.output_dir = output_dir

    def download(self):

        # Create data directory if it doesn't already exists
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
            logging.debug("Created data directory (%s)", self.output_dir)

        num_sources = len(self.dataset["sources"])
        index = 0

        # Read all sources in the dataset description an try to download them
        for source in self.dataset["sources"]:

            # TODO: Check if the resource has already been downloaded

            output_path = os.path.join(self.output_dir, source["name"])

            # Try to download the resource
            try:
                logging.info("Downloading element %d of %d (%s)", index + 1, num_sources, output_path)
                file = urllib.request.urlopen(source["url"])
                # Open output file and write content of resource to it
                open(output_path, "wb").write(file.read())

            except urllib.request.HTTPError as error:
                logging.error("HTTP Error (%d): Trying to download %s", error.code, source["name"])

            index += 1

        # Check if all resources have been downloaded
        logging.info("Successfully downloaded resources")

