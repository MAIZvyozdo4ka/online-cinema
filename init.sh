#!/bin/bash

cd "$(cd "$(dirname "$0")" && pwd)" || exit

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

mkdir -p dataset

curl -L -o ~/Downloads/archive.zip https://www.kaggle.com/api/v1/datasets/download/grouplens/movielens-20m-dataset
mv ~/Downloads/archive.zip "$(pwd)"
unzip archive.zip -d dataset
rm archive.zip

python3 filter.py