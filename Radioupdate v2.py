import vlc
import RPi.GPIO as GPIO
import time
import subprocess

prev_input = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)

p = vlc.MediaPlayer("https://playerservices.streamtheworld.com/api/livestream-redirect/KFWRFMAAC")
        
#run radio when the button on 24 is pressed


#check wifi and flash LED if not working 
while True:
    ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        print(output)
        GPIO.output(6, GPIO.HIGH)
        while True:
            input = GPIO.input(24)
            if ((not prev_input) and input):
                print("Switch Turned On")
                p.play()
                GPIO.output(12, GPIO.HIGH)
            prev_input = input
            time.sleep(0.05)
            input = GPIO.input(24)
            if ((not prev_input) and input == 0):
                print("Switch Turned Off")
                p.stop()
                GPIO.output(12, GPIO.LOW)
                prev_input = input
                time.sleep(1)
        
    except subprocess.CalledProcessError:
        # grep did not match any lines
        print("No wireless networks connected")
        GPIO.output(6, GPIO.HIGH)
        time.sleep (1)
        GPIO.output(6, GPIO.LOW)
        time.sleep (1)


