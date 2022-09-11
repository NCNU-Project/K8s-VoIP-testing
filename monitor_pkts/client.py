#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading
import subprocess
from time import sleep, time, ctime
import json

HOST = 'localhost'
PORT = 7000
TIMEOUT = 0.1  # sec
server_addr = (HOST, PORT)
case = 0
previous_IP = ""
current_handover_pod = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def execute_switchover():
    global current_handover_pod
    print("execute switchover code")
    if current_handover_pod == 0:
        subprocess.run('kubectl label pods rtpengine-daemonset-0 rtpengine-10.22.149.230-p0="False" --overwrite', capture_output=True, shell=True)
        subprocess.run('kubectl label pods rtpengine-daemonset-1 rtpengine-10.22.149.230-p0="True" --overwrite', capture_output=True, shell=True)
        current_handover_pod = 1
    else:
        subprocess.run('kubectl label pods rtpengine-daemonset-1 rtpengine-10.22.149.230-p0="False" --overwrite', capture_output=True, shell=True)
        subprocess.run('kubectl label pods rtpengine-daemonset-0 rtpengine-10.22.149.230-p0="True" --overwrite', capture_output=True, shell=True)
        current_handover_pod = 0

def wait_for_data():
    # wait for data that we subscribe
    global case, previous_IP
    send_obj = {"case": case, "time": str(time())}
    return_data = {}

    try:
        # print(send_obj)
        send_str = json.dumps(send_obj)
        s.sendto(send_str.encode(), server_addr)
        s.settimeout(TIMEOUT)
        indata, addr = s.recvfrom(1024)
        return_data = json.loads(indata.decode())
        if (return_data["IP"] != previous_IP):
            case += 1
            previous_IP = return_data["IP"]
            print("switch to next case")
            execute_switchover()

    except socket.error as socketerror:
        print("timeout!!")

while True:
    print(wait_for_data)
    t = threading.Thread(target=wait_for_data)
    t.start()
    # wait for a timeout for successful exit the process event the socket not get any data
    sleep(TIMEOUT)
    # more time for thread to tear down
    t.join(TIMEOUT)
