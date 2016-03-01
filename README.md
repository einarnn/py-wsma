# py-wsma

Simple example of how to put a (insecure) REST-like proxy in front of Cisco's SOAP-like WSMA interface on IOS/IOS-XE.

What we have here is:

* start.sh -- Simple script that creates a virtualenv and pulls in the packages required for app.py to work
* app.py -- A simple REST server built using Flask (at the same time as learning how to use Flask)
* WSMA.py -- A very simple and incomplete module to use WSMA to do some simple tasks.
* config.txt -- The (incomplete) config necessary on an IOS/IOS-XE box to enable WSMA with an HTTPS transport.
