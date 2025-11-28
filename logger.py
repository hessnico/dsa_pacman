import datetime


class Logger:
    def _ts(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def __init__(self, debug=False):
        self.debug_enabled = debug

    def set_debug(self, flag: bool):
        self.debug_enabled = flag

    def Debug(self, *msg):
        if self.debug_enabled:
            print(f"[{self._ts()}][DEBUG]", *msg)

    def Info(self, *msg):
        print(f"[{self._ts()}][INFO]", *msg)

    def Warn(self, *msg):
        print(f"[{self._ts()}][WARN]", *msg)

    def Error(self, *msg):
        print(f"[{self._ts()}][ERROR]", *msg)


log = Logger()
