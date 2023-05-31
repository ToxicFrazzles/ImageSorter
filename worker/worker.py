from .media_manager.media_manager import MediaManager
from .ws_auth import WSAuth
from .ws_ping import WSPing


class Worker:
    def __init__(self):
        self.manager = MediaManager()

    def run(self):
        try:
            self.manager.register_module(WSAuth(self.manager))
            self.manager.register_module(WSPing(self.manager))
            self.manager.run()
        except KeyboardInterrupt:
            pass
