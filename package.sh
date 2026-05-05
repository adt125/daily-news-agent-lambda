#!/bin/bash

set -euo pipefail

PYTHON_VERSION="${LAMBDA_PYTHON_VERSION:-3.13}"
PLATFORM="${LAMBDA_PLATFORM:-manylinux2014_x86_64}"

rm -rf build
mkdir build
rm -f lambda.zip

# AWS Lambda already includes boto3/botocore. Excluding them keeps the zip
# smaller and avoids bundling unnecessary AWS SDK files.
grep -vE '^(boto3|botocore|s3transfer)([<=> ].*)?$' requirements.txt > build/requirements-lambda.txt

pip3 install \
  --platform "$PLATFORM" \
  --implementation cp \
  --python-version "$PYTHON_VERSION" \
  --only-binary=:all: \
  --no-cache-dir \
  --no-compile \
  -r build/requirements-lambda.txt \
  -t build/

cp -r lambda/* build/

find build -type d -name "__pycache__" -prune -exec rm -rf {} +
find build -type d \( -name "tests" -o -name "test" -o -name "_tests" \) -prune -exec rm -rf {} +
find build -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
rm -rf build/bin
rm -f build/requirements-lambda.txt

cd build
zip -qr ../lambda.zip . \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x "*.pyo"
cd ..
