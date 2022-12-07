import threading
import time
import sys

class SecondCounter(threading.Thread):
    '''
    create a thread object that will do the counting in the background
    default interval is 1/1000 of a second
    '''
    def __init__(self, sentence, interval=2):
        # init the thread
        threading.Thread.__init__(self)
        self.interval = interval  # seconds
        # initial value
        self.value = 0
        # controls the while loop in method run
        self.alive = False
        self.sentence = sentence

    def run(self):
        '''
        this will run in its own thread via self.start()
        '''


        self.alive = True
        while self.alive:
            time.sleep(self.interval)
            self.sentence += " "
            print(self.sentence)
            # update count value

        # self.value += self.interval

    def peek(self):
        '''
        return the current value
        '''
        return self.value

    def finish(self):
        '''
        close the thread, return final value
        '''
        # stop the while loop in method run
        self.alive = False
        # return self.value


# create the class instance
# count = SecondCounter()

# start the count
# count.start()
