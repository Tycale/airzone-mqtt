Airzone-mqtt
============

Quick hack/fork of https://github.com/gpulido/python-airzone in order to
monitor/control Airzone via MQTT.


Install
-------

bash::

   cp airzone.service /etc/systemd/system/
   sudo apt-get install python-pip
   sudo python -m pip install --upgrade pip setuptools wheel
   sudo pip install -r requirements.txt
   sudo systemctl daemon-reload
   sudo systemctl enable airzone
   sudo systemctl start airzone

configuration
-------------

Copy env.sample as env and modify it according your setup.

openhab
-------

See openhab folder, note, the sample uses MQTT v1

-----

Python control of Innobus installation through Modbus serial Gateway & local API
================================================================================

|PyPI version|

A simple Python API for controlling and interfacing with an Airzone installation devices.
The systems currently supported:
   
- Innobus through modbus protocol.
- Aidoo through modbus protocol.
- Local API use on ethernet airzone controller like AIRZONE AZX6WEBSCLOUDC


.. |PyPI version| image:: https://badge.fury.io/py/python-airzone.svg
   :target: https://badge.fury.io/py/python-airzone


