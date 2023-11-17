import json
import os

from collections import UserDict

class Settings(UserDict):
    def __getattr__(self, name):
        return self.__getitem__(name.upper());

    def __getitem__(self, name):
        return super().__getitem__(name.upper())

    def __setitem__(self, name, value):
        name = name.upper()
        super().__setitem__(name, Settings(value) if isinstance(value, dict) else value)
    
    def load(self, pathlist: list):
        for path in pathlist:
            if os.path.exists(path):
                with open(path) as f:
                    # this is a bit dangerous, we should not trust config files
                    self.update(json.load(f))

settings = Settings({
    "DB_HOST": os.getenv("DB_HOST", "localhost:8080"),
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "ERROR"),
    "MQ_HOST": os.getenv("MQ_HOST", "mq"),
    "MQ_EXCHANGE": os.getenv("MQ_EXCHANGE", "zhaw-km"),
    "MQ_QUEUE": os.getenv("MQ_QUEUE", "departmentqueue"),
    "MQ_BINDKEYS": list([routing_key.strip() for routing_key in os.getenv("MQ_BINDKEYS", "importer.person").split(",")]),
    "MQ_HEARTBEAT": int(os.getenv("MQ_HEARTBEAT", 6000)),
    "MQ_TIMEOUT": int(os.getenv("MQ_TIMEOUT", 3600)),
    "MQ_USER": os.getenv("MQ_USER", "resolver-department"),
    "MQ_PASS": os.getenv("MQ_PASS", "guest")
})
