import time
import psutil
from client_license import verify, FLOATING_INTERVAL
from subprocess import Popen, PIPE

class MainProgram():
    def __init__(self) -> None:
        self.encoding = "utf-8"
        self.proc_list = {}
        self.camera_list = ['cam01','cam02']
    
    def __run_all(self):
        self.__run_detect()
        time.sleep(2)
        self.__run_gateway()
        time.sleep(20)
        self.__run_ai_main()
        time.sleep(2)
    
    def __stop(self):
        try:
            for _, process in self.proc_list.items():
                process.kill()
                process.wait()
        except: pass
    
    def __run_gateway(self):
        for p in psutil.process_iter():
            if p.cmdline() == ["python3", "gateway.py"]:
                return
        gateway = Popen(["python3", "gateway.py"], stdin=PIPE, encoding=self.encoding)
        self.proc_list[gateway.pid] = gateway
    def __run_detect(self):
        for p in psutil.process_iter():
            if p.cmdline() == ["python3", "shell.py","server_detect"]:
                return
        detect_server = Popen(["python3", "shell.py","server_detect"], stdin=PIPE, encoding=self.encoding)
        self.proc_list[detect_server.pid] = detect_server
    def __run_ai_main(self):
        for p in psutil.process_iter():
            if p.cmdline() == ["python3", "app.py", "--camid", "cam01"] or p.cmdline() ==["python3", "app.py", "--camid", "cam02"] :
                return
        ai_main1 = Popen(["python3", "app.py","--camid", "cam01"], stdin=PIPE, encoding=self.encoding)
        ai_main2 = Popen(["python3", "app.py","--camid", "cam02"], stdin=PIPE, encoding=self.encoding)
        self.proc_list[ai_main1.pid] = ai_main1
        self.proc_list[ai_main2.pid] = ai_main2
       
    def _start(self):
        if verify():
            self.__run_all()
        else:
            print("Not activated!")
        
        while(True):
            try:
                time.sleep(FLOATING_INTERVAL)
                if not verify():
                    self.__stop()
                    continue
                
                self.__run_all()
            except:
                self.__stop()
                break

if __name__ == "__main__":
    m = MainProgram()
    m._start()
