#!/usr/bin/env python3
import argparse

import airzone
import json

import paho.mqtt.client as mqtt
import time
import logging
import os, sys

AZ_TOPIC = "airzone/events"


def action(args):
    extra_args = {"use_rtu_framer": args.rtuframer}
    az = airzone.airzone_factory(args.address, args.port, args.machine, args.system, **extra_args)

    if 'log' in args:
        logging.basicConfig(level=logging.DEBUG, filename=args.log, format="%(asctime)s %(message)s", filemode="w")
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(asctime)s %(message)s")

    logger = logging.getLogger()

    logger.warning("successfully started the script")

    def on_connect(client, userdata, flags, rc):
        client.subscribe("airzone/actions/#")

    def on_message(client, userdata, message):
        topic = message.topic
        # TBD

    mqttc = mqtt.Client(client_id=args.mqtt_client)
    if args.mqtt_username and args.mqtt_password:
        logger.info('MQTT username and password provided')
        mqttc.username_pw_set(args.mqtt_username, password=args.mqtt_password)
    mqttc.connect(args.mqtt_address, port=args.mqtt_port, keepalive=60)

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect

    #start the client
    mqttc.loop_start()

    # Monitoring loop
    while True:
        try:
            jsonStatus = az.toJSON()
            status = json.loads(jsonStatus)
            logger.debug(status)
            mqttc.publish('{}/mode'.format(AZ_TOPIC), payload=status['mode'], retain=True)
            for z in status['zones']:
                logger.debug(z)
                topic_prefix = '{}/{}'.format(AZ_TOPIC, z['name'])
                mqttc.publish('{}/temp'.format(topic_prefix), payload=z['temp'], retain=True)
            time.sleep(60)
        except (EOFError, SystemExit, KeyboardInterrupt):
            mqttc.disconnect()
            sys.exit(1)


parser = argparse.ArgumentParser(prog='airzone')
parser.add_argument("address", type=str, help="serial device or ip address for localapi")
parser.add_argument("port", type=str, help="serial tcp port or http port for localapi")
parser.add_argument("mqtt_address", type=str, help="mqtt ip address")
parser.add_argument("mqtt_client", type=str, help="mqtt client id")
parser.add_argument("--mqtt_port", type=int, help="mqtt ip port", default=1883)
parser.add_argument("--mqtt-username", type=str, help="MQTT username")
parser.add_argument("--mqtt-password", type=str, help="MQTT password")
parser.add_argument("--log", type=str, help="logging file")
parser.add_argument("--machine", type=int, default=1, help="Machine number where connect")
parser.add_argument("--system", choices=['innobus', 'aido', 'localapi'], default='localapi', help="Type of Airzone System")
parser.add_argument("--state", choices=['str', 'raw', 'json'], default='json',
                    help="Get the formatted state, or the raw machine state")
parser.add_argument("--rtuframer", type=bool, default= False, help="use rtu framer for modbus.")
parser.set_defaults(func=action)

args = parser.parse_args()
args.func(args)
