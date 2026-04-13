#!/bin/bash

rm -rf venv

python3 -m venv venv

source venv/bin/activate

pip list

pip install mkdocs-material

pip install -r requirements.txt
