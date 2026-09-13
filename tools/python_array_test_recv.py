#!/usr/bin/env python3

from plane_pymavlink import mavutil

master = mavutil.mavlink_connection("udp::14555", dialect="array_test")

while True:
    m = master.recv_msg()
    if m is not None:
        print(m)
