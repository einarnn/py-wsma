#!/bin/sh

#
# bootstrap the virtual env if necessary
#
if [ -f "v/bin/activate" ]
then
    echo virtual env already created
    source v/bin/activate
else
    virtualenv v
    source v/bin/activate
    pip install jinja2 lxml flask
fi

#
# run the data server
#
python app.py

