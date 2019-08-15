class Config():
    def __init__(self, connectionString):
        self.config = dict(map(lambda x: x.split('=', 1), connectionString.split(';',2)))

    @property
    def hub_address(self):
        return self.config['HostName']

    @property
    def device_id(self):
        return self.config['DeviceId']

    @property
    def shared_access_key(self):
        return self.config['SharedAccessKey']