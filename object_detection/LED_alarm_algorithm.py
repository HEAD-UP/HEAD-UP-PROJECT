import threading
import RPi.GPIO as GPIO
import time

def warning_on():
    global timer, danger, end
    while not end:
        if danger:
            timer = 5
        elif timer == 0:
            GPIO.output(10, False)

        if timer > 0:
            print("Time : ", timer)
            GPIO.output(10, True)
            time.sleep(1)
            timer -= 1
    GPIO.output(10, False)

def socket_input(num):
    global danger
    if int(num) == 1:
        danger = True
    elif int(num) == 0:
        danger = False

def thread_end(t):    
    global end
    end = True
    t.join()
    print("thread end")
    
def init():
    global timer, danger, end
    #9 : green # 10 : red # 11: blue
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(9, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    
    end = False
    danger = False
    timer = 0

    t = threading.Thread(target=warning_on, args = ())
    t.start()
    return t

# for local debug
if __name__ == '__main__':
    th_input = init()
    while True:
        temp = input()
        if temp == 3:
            break
        else :
            socket_input(temp)
    thread_end(th_input)

