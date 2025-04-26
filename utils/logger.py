import sys
import threading
from datetime import datetime

class SyncLogger:
    def __init__(self, log_file, to_stdout=True):
        self.log_file = log_file
        self.to_stdout = to_stdout
        self.logs = []
        self.lock = threading.Lock()

    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {msg}"
        
        with self.lock:
            self.logs.append(log_msg)
            if self.to_stdout:
                print(log_msg)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_msg + "\n")

    def get_logs(self):
        return "\n".join(self.logs) 