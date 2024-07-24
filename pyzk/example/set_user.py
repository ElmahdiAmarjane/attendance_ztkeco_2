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

def setup_new_employee(entry_username,telephone):
    
    conn = None
    zk = ZK(DEVICE_IP, port=DEVICE_PORT, verbose=VERBOSE, timeout=5, password=0, force_udp=False, ommit_ping=False)


    try:
        conn = zk.connect()  # Establish connection to the fingerprint scanner
        db_controller.delete_employees_without_fingerprint()
        try:
         user = db_controller.create_employee(entry_username,telephone)
        # Setting up a new user
        except Exception as e:
         print(e)
         return e
        
        try:
         conn.set_user(uid=user[0], name=user[1], privilege=const.USER_DEFAULT, password='', group_id='', user_id='')
         conn.enroll_user(user[0])
        except  Exception  as e:
         print(e)
         return e
           


        print("👍testtets :")
        print("🦍🦍",conn.get_users())
        template = conn.get_user_template(uid=user[0])
        print("👍mark fingerprint : ",type(template.mark))
        db_controller.update_template_for_employee(user[0],template.mark)
        return True
    except Exception as e:
        print(f"Process terminated: {e}")
        return e
    finally:
        if conn:
            conn.disconnect()  # Disconnecting from the fingerprint scanner if connected

