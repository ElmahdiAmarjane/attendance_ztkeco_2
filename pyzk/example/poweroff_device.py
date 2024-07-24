# -*- coding: utf-8 -*-
import os
import sys
from device_infos import DEVICE_IP, DEVICE_PORT, VERBOSE

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK


conn = None
zk = ZK(DEVICE_IP, port=DEVICE_PORT)
try:
    conn = zk.connect()
    print ("Shutdown the device...")
    conn.poweroff()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
