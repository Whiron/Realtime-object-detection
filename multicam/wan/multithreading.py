#Python multithreading example to demonstrate locking.
#1. Define a subclass using Thread class.
#2. Instantiate the subclass and trigger the thread. 
#3. Implement locks in thread's run method. 

from __future__ import print_function
from threadrealtimedetection import TRealtimeObjectDetection
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import threading
import datetime
import cv2


exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        # Acquire lock to synchronize thread
        threadLock.acquire()
        print_date(self.name, self.counter)
        #line(number)
        # Release lock for the next thread
        threadLock.release()
        print ("Exiting " + self.name)

    
def line(tNumber,number):
        #number = 7
        #number = number
        #threadLock.acquire()
        while (number > 0):
            threadLock.acquire()
            print (tNumber ," is at " , number)
            number = number - 1
            threadLock.release()
            # time.sleep(0.1)
        #threadLock.release()
        # Release lock for the next thread

def print_date(threadName, counter):
    datefields = []
    today = datetime.date.today()
    datefields.append(today)
    print ("%s[%d]: %s" % ( threadName, counter, datefields[0] ))

threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = myThread("Thread", 1)
thread2 = myThread("Thread", 2)

#arguments to run
n1=10
n2=5
thread1 = threading.Thread(target=line, args=(1,n1,))
thread2 = threading.Thread(target=line, args=(2,n2,))

# Start new Threads
thread1.start()
thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print ("Exiting the Program!!!")