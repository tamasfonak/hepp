#!/usr/bin/env python2

# Modified jonnyalpha code by jehutting
# See jonnyalpha's code at will price python-omxplayer-wrapper issue #90
# Original code uses gpiozero's PIR in stead of keyboard keys.
# Removed also unused camera code.
# Makes use of user longagofaraway "Allow control of multiple instances via dbus #89"
# pull request!

import os
import sys
from time import sleep
from omxplayer import OMXPlayer
#from gpiozero import MotionSensor
from signal import pause

#pir = MotionSensor(23)
#pir.when_motion = motion_detected
#pir.when_no_motion = no_motion
# The motion sensor is simulated by KEYBOARD
from keyb import KBHit
kb = KBHit()

videos = './'
adev='hdmi'
vid1 = OMXPlayer(videos+'/Vid_Wait_Loop.mp4',args=['--no-osd', '--no-keys', '--win', '100 100 640 480', '--loop', '-o', adev], dbus_name='org.mpris.MediaPlayer2.omxplayer1', pause=True)

def main():
    try:  # was missing in original code
        initiate()
        print("playing vid1")
        vid1.play()

        while True:
            # keyboard PIR simulation
            if kb.kbhit():
                c = kb.getch()
                if c == chr(27) or c == 'q': # ESC or 'q' key to exit the program
                    print("terminated by user using ESC or 'q'")
                    break
                elif c == 'm': # key 'm' simulates the pir's when_motion callback 
                    motion_detected()
                # uncomment following code when vid1 is not to resume after vi2 completion
                # see motion_detected
                #elif c == 'n': # key 'n' simulates the pir's when_no_motion callback 
                #    no_motion()
            sleep(1)
    except KeyboardInterrupt:
        print("terminated by user using Ctrl+C")
    finally:
        vid1.quit()
        #vid2.quit()
    print("bye bye")

def initiate():
    print("CENTRAL AI Startup - Running initial setup")
    sleep(1)
    print("Starting Central AI visual front end")
    sleep(1)
    print("Motion detection activated")
    sleep(1)
    print("Security system activated")

def no_motion():
    print("All quiet")
    # comment following code when vid1 is to resume after vid2 completion
    # see motion_detected
    #print("Playing Vid_Wait_Loop")
    #vid1.play() # = un-pausing

def motion_detected():
    print("Intruder Detected")
    #sleep(2)
    print("Pausing loop")
    vid1.pause()
    print("Playing Vid_Name_Hammerstein")
    vid2 = OMXPlayer(videos+'/Vid_Name_Hammerstein.mp4',args=['--no-osd', '--no-keys', '--win', '100 100 640 480', '--layer', '10',
                     '-o', adev], dbus_name='org.mpris.MediaPlayer2.omxplayer2', pause=True)
    vid2.play_sync()
    # Once the playing of vid2 is finished (the real) OMXPlayer terminates.
    # Sending commands to vid2 will fail!
    # uncomment following code to resume playing vid1 after vid2 completion
    print("Playing Vid_Wait_Loop")
    vid1.play() # = un-pausing
    

if __name__ == '__main__': 
    main()
