# -*- coding: utf-8 -*-
import sys
sys.path.append("zk")
from example.device_infos import DEVICE_IP, DEVICE_PORT, VERBOSE

from zk import ZK, const

conn = None
zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
    print ('Connecting to device ...')
    conn = zk.connect()
    print ('Disabling device ...')
    conn.disable_device()
    print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
    # print '--- Get User ---'
    users = conn.get_users()
    for user in users:
        privilege = 'User'
        if user.usertype() == const.USER_ADMIN:
            privilege = 'Admin'
        elif user.usertype() == const.USER_MANAGER:
            privilege = 'Manager'
        elif user.usertype() == const.USER_ENROLLER:
            privilege = 'Enroller'
        if user.is_disabled():
            privilege += '(DISABLED)'
        print ('- UID #{}'.format(user.uid))
        print ('  Name       : {}'.format(user.name))
        print ('  Privilege  : {}'.format(privilege))
        print ('  Password   : {}'.format(user.password))
        print ('  Group ID   : {}'.format(user.group_id))
        print ('  User  ID   : {}'.format(user.user_id))

    print ("Voice Test ...")
    conn.test_voice()
    print ('Enabling device ...')
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
