#!/bin/sh
# sudo mount -o rw,remount / # Remount drive if locked
# source venv/bin/activate   # Activate venv
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z" # Retrieve date
flask run --host=0.0.0.0  # Run flask