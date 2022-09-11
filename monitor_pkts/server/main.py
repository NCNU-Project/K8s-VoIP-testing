#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import socket
from time import sleep
import json
import logging
import threading

HOST = '0.0.0.0'
PORT = 7000
TIMEOUT = 0.1
case = -1


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

def main():
    # get local ip
    main_ip = extract_ip()
    global case

    while True:
        indata, addr = s.recvfrom(1024)
        in_obj = json.loads(indata.decode())
        if in_obj["case"] != case:
            print(indata)
            case = in_obj["case"]
        out_obj = {"IP": main_ip}
        outdata = json.dumps(out_obj)
        s.sendto(outdata.encode(), tuple(addr))
        sleep(TIMEOUT)

if __name__ == '__main__':
    main()
