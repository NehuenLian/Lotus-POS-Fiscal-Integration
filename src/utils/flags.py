class FlagManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection_exists = False

        return cls._instance
    
    @property
    def connection_exists(self):
        return self._connection_exists
    
    @connection_exists.setter
    def connection_exists(self, value):
        if not isinstance(value, bool):
            raise ValueError("")
        self._connection_exists = value
