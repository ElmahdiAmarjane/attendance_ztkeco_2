# -*- coding: utf-8 -*-
import os
import sys
import time

import controller as db_controller
from .device_infos import DEVICE_IP, DEVICE_PORT, VERBOSE
import uuid
from zk import ZK, const

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

def setup_new_employee(entry_username, telephone, retry_count=3):
    zk = ZK(DEVICE_IP, port=DEVICE_PORT, verbose=VERBOSE, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = None

    # Attempt to connect to the device
    for attempt in range(retry_count):
        try:
            conn = zk.connect()  # Establish connection to the fingerprint scanner
            break  # Connection successful, exit the loop
        except Exception as e:
            print(f"Error connecting to device (attempt {attempt + 1}/{retry_count}): {e}")
          #  time.sleep(2)  # Wait for 2 seconds before retrying
    else:
        return "errorConnection"  # Return error if connection fails after all attempts

    try:
        # Perform device operations if connected
        db_controller.delete_employees_without_fingerprint()

        try:
            user = db_controller.create_employee(entry_username, telephone)
        except Exception as e:
            print(f"Error creating employee: {e}")
            return "errorCreateEmployee"

        try:
            conn.set_user(uid=user[0], name=user[1], privilege=const.USER_DEFAULT, password='', group_id='', user_id='')
            conn.enroll_user(user[0])
        except Exception as e:
            print(f"Error saving fingerprint: {e}")
            return "errorSavingFingerPrint"

        template = conn.get_user_template(uid=user[0])
        print(f"Fingerprint template type: {type(template.mark)}")
        db_controller.update_template_for_employee(user[0], template.mark)
        return "success"

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "errorConnection"  # Handle unexpected errors by returning errorConnection

    finally:
        if conn:
            conn.disconnect()  # Disconnecting from the fingerprint scanner if connected
