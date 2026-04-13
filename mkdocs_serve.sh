#!/bin/bash

#python -m pip install mkdocs
#python -m pip install mkdocs-material

python3 -m venv venv

source venv/bin/activate

mkdocs serve

# http://127.0.0.1:8000/mobile-id-wallet-documentation/
