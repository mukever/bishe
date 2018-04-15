
import threading
import time
import inspect
import ctypes

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

class TestThread(threading.Thread):
    def run(self):
        print ("begin")
        while True:
            time.sleep(0.2)
            print('.','.')
        print ("end")

    ##将每次训练任务放到一个独立的线程中进行，实现多线程
    def startTrain(self):
        # refreshParam()
        self.__threadTrain = threading.Thread(target=self.trainmodel)
        self.train_flag = False
        self.__threadTrain.setDaemon(True)
        self.__threadTrain.start()
        #        self.currentthread = self.__threadTrain.getName()
        if not self.train_flag:
            self.periodicTextCall()
        else:
            self.canvas.show()
            self.__threadTrain.stop()
            self.__threadTrain.join()
            self.__threadTrain.exit()

        return self.__threadTrain

    def stop_trainthread(self):
        trainingthread = self.__threadTrain
        self._async_raise(trainingthread.ident, SystemExit)
        self.StateQueue.put("train stopped.")
        self.train_flag = True
        print('train stopped.')
if __name__ == "__main__":
    t = TestThread()
    t.start()

    print(t.name)
    print(t.ident)
    id = t.ident

    time.sleep(1)
    stop_thread(t)
    print ("stoped")