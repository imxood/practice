#!/bin/bash

pip3 uninstall -y log_server

rm -rf build/ dist/ log_server.egg-info/

python3 setup.py sdist

cd dist

pip3 install --user log_server-0.1.tar.gz
