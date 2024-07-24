# -*- coding: utf-8 -*-
import os
import sys


from .device_infos import DEVICE_IP, DEVICE_PORT, VERBOSE
from controller import log_entry_exit

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK

def live_capture():
 conn = None
 zk = ZK(DEVICE_IP, port=DEVICE_PORT)
 try:
    conn = zk.connect()
    print("test")
    for attendance in conn.live_capture():
        if attendance is None:
            
            pass
            print ("nothing to print ")
        else:
            print("👽👽",conn.get_attendance())
            print (attendance.get_time(),"status ::: ",attendance.punch)
            log_entry_exit(attendance)
         
        
       
 except Exception as e:
    print ("Process terminate : {}".format(e))
 finally:
    if conn:
        conn.disconnect()
