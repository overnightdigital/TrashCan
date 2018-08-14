#!/usr/bin/python
import SmartTrash as trash
import config
import Simulator as simulator
from thread import start_new_thread

start_val = 1

num_threads = 1
max_TrashCans = 5

count = input("Please enter the amount of Trash Cans to be simulated(Max 5): ")
print(str(count) + " Trash cans will be simultated")

if count > max_TrashCans:
        count = 5

try:
        start_new_thread(trash.main, (simulator.get_RawValue(), config.oauth_credentials_for_device0, config.device_id0,))
        for x in range(1, count):
                if x == 1:
                        start_new_thread(trash.main, (start_val, config.oauth_credentials_for_device1, config.device_id1,))
                if x == 2:
                        start_new_thread(trash.main, (start_val, config.oauth_credentials_for_device2, config.device_id2,))
                if x == 3:
                        start_new_thread(trash.main, (start_val, config.oauth_credentials_for_device3, config.device_id3,))
                if x == 4:
                        start_new_thread(trash.main, (start_val, config.oauth_credentials_for_device4, config.device_id4,))

except:
        print("Error: unable to start thread")
        
while num_threads > 0:
        pass