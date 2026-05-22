#!/bin/bash

set -e

lsof -ti :8000 | xargs kill -9

if [ ! -d "venv" ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi

mkdocs serve

# http://127.0.0.1:8000/mobile-id-wallet-documentation/
