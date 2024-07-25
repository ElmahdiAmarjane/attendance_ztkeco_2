# -*- coding: utf-8 -*-
import os
import sys

# from .database.create_user import create_user

import  controller as db_controller
from .device_infos import DEVICE_IP, DEVICE_PORT, VERBOSE
import uuid
CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK, const

def get_attendence():
    
    conn = None
    zk = ZK(DEVICE_IP, port=DEVICE_PORT, verbose=VERBOSE, timeout=5, password=0, force_udp=False, ommit_ping=False)

    try:
        conn = zk.connect()  # Establish connection to the fingerprint scanner
    
        try:
          results = conn.get_attendance()

          db_controller.insert_attendance(results)

        except Exception as e:
         print(e)
         return e
    except Exception as e:
         print("connection faild .")
    finally:
        if conn:
            conn.disconnect()  # Disconnecting from the fingerprint scanner if connected

