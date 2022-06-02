from threading import Thread
from time import sleep

class ServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            for num in range(0, 1000):
                print(num)
            sleep(1)
            print('loop complete')

thread = ServerThread()
thread.start()
thread.join()