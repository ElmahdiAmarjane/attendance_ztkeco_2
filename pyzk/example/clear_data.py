# -*- coding: utf-8 -*-
import os
import sys

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK
from device_infos import DEVICE_IP, DEVICE_PORT, VERBOSE


conn = None
zk = ZK(DEVICE_IP, port=DEVICE_PORT)
try:
    conn = zk.connect()
    choices = raw_input('Are you sure want to delete all data? [Y/N]: ')
    if choices == 'Y':
        print ("Clear all data...")
        conn.clear_data()
    else:
        print ("Clear all data canceled !")
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
