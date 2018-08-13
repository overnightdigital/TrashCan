#!/usr/bin/python
import SmartTrash as trash
import Simulator as simulator
import config
from thread import start_new_thread

num_threads = 1

try:
        start_new_thread(trash.main, (simulator.get_SimulatedValue(), config.oauth_credentials_for_device0, config.device_id0,))
        start_new_thread(trash.main, (45, config.oauth_credentials_for_device1, config.device_id1,))
except:
        print("Error: unable to start thread")
        
while num_threads > 0:
        pass