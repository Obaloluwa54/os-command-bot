import os
from datetime import datetime
from core.config import LOGS_DIR, MAX_LOGS

class LogManager:
    def __init__(self):
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

    def save_log(self, tool, output):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{tool}_{timestamp}.log"
        path = os.path.join(LOGS_DIR, filename)
        with open(path, "w") as f:
            f.write(output)
        self.cleanup_logs()
        return path

    def list_logs(self):
        return [f for f in os.listdir(LOGS_DIR) if f.endswith(".log")]

    def read_log(self, filename):
        path = os.path.join(LOGS_DIR, filename)
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        return "Log not found."

    def cleanup_logs(self):
        logs = sorted(self.list_logs())
        if len(logs) > MAX_LOGS:
            for log in logs[:len(logs)-MAX_LOGS]:
                os.remove(os.path.join(LOGS_DIR, log))
