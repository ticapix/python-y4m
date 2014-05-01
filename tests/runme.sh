#!/bin/sh

cd $(dirname $0)
export PYTHONPATH=`pwd`/..

python2.7 tests.py
python3.3 tests.py
python3.4 tests.py
