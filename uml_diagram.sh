#!/bin/bash
#
# requires:
# - bash shell
# - pip install pylint
#
mkdir -p uml_diagram
pyreverse -o png -p PythonLearningGame ./src -d uml_diagram
