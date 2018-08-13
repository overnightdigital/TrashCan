import time
import json
import RPi.GPIO as GPIO
import datetime
import urllib3
import config


    
def main(simulated_value, oauth_credentials_for_devicex, device_idx):
        # if the simulated value is -99 that means we are using the main device data
        '''****************************************************************************************
        HCP services Variables
        ****************************************************************************************'''
        http = urllib3.PoolManager()
        headers = urllib3.util.make_headers(user_agent=None)
        headers['Authorization'] = 'Bearer ' + oauth_credentials_for_devicex
        headers['Content-Type'] = 'application/json;charset=utf-8'
        url='https://iotmms' + config.hcp_account_id + config.hcp_landscape_host + '/com.sap.iotservices.mms/v1/api/http/data/'+ str(device_idx)
        urllib3.disable_warnings()


        '''****************************************************************************************
        Pin Configurations
        ****************************************************************************************'''
        TRIG = 18 # Broadcom pin 18 (P1 pin 12)                                          
        ECHO = 24 # Broadcom pin 23 (P1 pin 16)                                          
        LIDCOVER = 15
        alarmOut = 22 # Broadcom pin 22 (P1 pin 15) 

        '''****************************************************************************************
        Function Name 	:	ultrasonicSensorInit()
        Description		:	Function which initilizes the GPIO pins
        Parameters 		:	-
        ****************************************************************************************'''

        def ultrasonicSensorInit():
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(TRIG,GPIO.OUT)
                GPIO.setup(ECHO,GPIO.IN)
                GPIO.setup(LIDCOVER,GPIO.IN)
                GPIO.setup(alarmOut,GPIO.OUT)
                GPIO.output(TRIG, False)
                GPIO.output(alarmOut,False)
                
                
        '''****************************************************************************************
        Function Name 	:	distanceMeasurement()
        Description		:	Function calculates the amount of waste in the trashcan and send it to the client
                                                and sends an alert message when trash can reaches the threshold
        Parameters 		:	-
        ****************************************************************************************'''
        currentDistance = 0
        LOOP_SAMPLING_TIME = 2
        CRITICAL_DISTANCE = 100
        NOTIFICATION_TIME_DELAY = 15
        lidCoverSendMessage0 = True
        lidCoverSendMessage1 = True



        try:
                start = 0
                l_prev_distance = 0
                ultrasonicSensorInit()
                while 1:
                        # print("in loop 1")
                        if GPIO.input(LIDCOVER) == 0:
                                # print("in loop 2")
                                if(lidCoverSendMessage0 == True):
                                        # print("in loop 3")
                                        lidCoverSendMessage1 = True
                                        timestamp= int(time.time())	
                                        body= '{"mode":"async", "messageType":"' + str(config.message_type_id_isOpen) + '", "messages":[{"timestamp":'+ ' "' + str(timestamp) + '"'+ ', "isOpen": 0 }]}'
                                        r = http.urlopen('POST', url, body=body, headers=headers)
                                        print(body)
                                        print(r.data)
                                        lidCoverSendMessage0= False
                                time.sleep(LOOP_SAMPLING_TIME)		
                                GPIO.output(TRIG, True)
                                time.sleep(0.00001)
                                GPIO.output(TRIG, False)
                                #Starts the timer 
                                while (GPIO.input(ECHO)==0):
                                    start = time.time()
                                    # print("while 1")
                                #Waits for the timer to end once the pin is high
                                while GPIO.input(ECHO)==1:
                                        end = time.time()
                                        # print("while 2")
                                pulse_duration = end - start
                                l_distance = pulse_duration * 17150
                                l_distance = round(l_distance, 2)
                                if simulated_value != -99: 
                                        l_distance = simulated_value
                                currentDistance = l_distance
                                timestamp= int(time.time())			
                                body= '{"mode":"async", "messageType":"' + str(config.message_type_id_Distance) + '", "messages":[{"timestamp":' + '"' + str(timestamp) + '"'+ ', "distance":"' + str(l_distance) + '"}]}'
                                r = http.urlopen('POST', url, body=body, headers=headers)
                                print(body)
                                print(r.data)
                                if currentDistance < 50:
                                    GPIO.output(alarmOut,True)
                                else:
                                    GPIO.output(alarmOut,False)
                        else:
                                if(lidCoverSendMessage1 == True):
                                        # print("error")
                                        timestamp= int(time.time())	
                                        body= '{"mode":"async", "messageType":"' + str(config.message_type_id_isOpen) + '", "messages":[{"timestamp":' + '"' + str(timestamp) + '"'+ ', "isOpen": 1 }]}'
                                        r = http.urlopen('POST', url, body=body, headers=headers)
                                        lidCoverSendMessage1= False
                                        lidCoverSendMessage0= True
                                        print(body)
                                        print(r.data)
        except KeyboardInterrupt: 
                        GPIO.cleanup()
