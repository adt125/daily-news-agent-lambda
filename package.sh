#!/bin/bash

rm -rf build
mkdir build

pip3 install -r requirements.txt -t build/

cp -r lambda/* build/

cd build
zip -r ../lambda.zip .
cd ..