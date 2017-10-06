import os
import logging
import urllib.request


class Downloader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.queue = []

    def add_to_queue(self, name, url, file_extension):
        self.queue.append((name, url, file_extension))

    def download(self):

        # Create data directory if it doesn't already exists
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)
            logging.debug("Created data directory (%s)", self.data_dir)

        # TODO: Check if the resource has already been downloaded

        # Iterate over all elements in the queue
        for i in range(len(self.queue)):

            resource = self.queue[i]
            output_path = os.path.join(self.data_dir, resource[0] + "." + resource[2])

            # Try to download the resource
            try:
                logging.info("Downloading element %d of %d in queue (%s)", i + 1, len(self.queue), output_path)
                file = urllib.request.urlopen(resource[1])
                # Open output file and write content of resource to it
                open(output_path, "wb").write(file.read())

            except urllib.request.HTTPError as error:
                logging.error("HTTP Error (%d): Trying to download %s", error.code, resource[1])

        # Check if all resources have been downloaded
        logging.info("Successfully downloaded resources in queue")
        # Delete all resources from queue
        self.queue.clear()
