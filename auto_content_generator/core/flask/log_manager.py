class LogManager:
    def __init__(self, max_entries=100):
        self.app_logs = []
        self.MAX_LOG_ENTRIES = max_entries
        self.stop_signal = False

    def append_log(self, message):
        if len(self.app_logs) >= self.MAX_LOG_ENTRIES:
            self.app_logs.pop(0)
        self.app_logs.append(message + "\n")

    def set_stop_signal(self, signal):
        self.stop_signal = signal