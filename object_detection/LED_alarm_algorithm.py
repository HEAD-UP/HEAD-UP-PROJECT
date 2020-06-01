import threading
import RPi.GPIO as GPIO
import time

#9 : green 10 : red 11: blue
GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

def warning_on():
    global timer, stime, sign_is_on
    
    while True:
        if timer > 0:
            print("timer : " + str(timer))
            sign_is_on = True
            stime = time.time()
            GPIO.output(10, True)
            time.sleep(timer)
            GPIO.output(10, False)
            sign_is_on = False
            
        else:
            pass
            
        
def input_cmd():
    global danger
    
    while True:
        num = int(input("put input : "))
        
        if num == 1:
            danger = True
            
        elif num == 2:
            danger = False
            
        else:
            break
        
    2

danger = False #false = not danger / true = danger

timer = 0
stime = 0
sign_is_on = False

gtime = time.time()

t = threading.Thread(target=warning_on, args = ())
std = threading.Thread(target=input_cmd, args = ())

t.start()
std.start()

danger = True

while True:
    
    if danger and not sign_is_on:
        timer = 5
        
        
    elif danger and sign_is_on:
        dtime = time.time()    
        
    elif not danger and sign_is_on:
        timer = int(dtime) - int(stime)
    
    '''
    if danger:
        if sign_is_on:
            dtime = time.time()
            
        else:
            timer = 5
            sign_is_on = True
            
    else:
        if sign_is_on:
            timer = int(dtime) - int(stime)
            
        else:
            pass
            '''
        
    
        
# not danger and not sign_is_on : pass       
        
    
    
    
        
    
    
    
    
    
    
    
    
