#! /bin/bash
BASEDIR=$(dirname "$0")
cd $BASEDIR
#source env/bin/activate
python3.4 main_app.py --sub $1
