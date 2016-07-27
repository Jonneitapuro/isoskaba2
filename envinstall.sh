#!/bin/bash
virtualenv --no-site-packages --distribute -p python3 .env && 
source .env/bin/activate && 
pip install -r requirements.txt
