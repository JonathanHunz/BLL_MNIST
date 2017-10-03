.PHONY: clean data lint requirements download_data

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

#################################################################################
# COMMANDS                                                                      #
#################################################################################

# Install Python dependencies using conda
requirements:
	conda install --file requirements.txt

# Make dataset
data: requirements download_data
	# Run the prepare_dataset.py script
	$(PYTHON_INTERPRETER) src/data/prepare_dataset.py

# Delete all compiled Python files
clean:
	find . -name "*.pyc" -exec rm {} \;

# Lint using flake8
lint:
	flake8 --exclude=lib/,bin/,docs/conf.py .

# Download raw data
download_data:
	# TODO: Implement download_data task