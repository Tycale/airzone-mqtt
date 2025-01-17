#!/usr/bin/env python3
import argparse

import airzone
import json


def action(args):
    extra_args = {"use_rtu_framer": args.rtuframer}
    m = airzone.airzone_factory(args.address, args.port, args.machine, args.system, **extra_args)
    if args.state == 'json':
        print(m.toJSON())
    elif args.state == 'str':
        print(str(m))
    else:
        print(str(m.machine_state))


parser = argparse.ArgumentParser(prog='airzone')
parser.add_argument("address", type=str, help="serial device or ip address for localapi")
parser.add_argument("port", type=str, help="serial tcp port or http port for localapi")
parser.add_argument("--machine", type=int, default=1, help="Machine number where connect")
parser.add_argument("--system", choices=['innobus', 'aido', 'localapi'], default='localapi', help="Type of Airzone System")
parser.add_argument("--state", choices=['str', 'raw', 'json'], default='json',
                    help="Get the formatted state, or the raw machine state")
parser.add_argument("--rtuframer", type=bool, default= False, help="use rtu framer for modbus.")
parser.set_defaults(func=action)

args = parser.parse_args()
args.func(args)
