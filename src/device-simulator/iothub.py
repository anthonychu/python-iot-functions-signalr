import base64
import hmac
import urllib.parse
import time

class IotHub():

    def __init__(self, hub_address, device_id, shared_access_key):
        self.shared_access_key = shared_access_key
        self.endpoint = hub_address + '/devices/' + device_id
        self.hub_user = hub_address + '/' + device_id
        self.hub_topic_publish = 'devices/' + device_id + '/messages/events/'
        self.hub_topic_subscribe = 'devices/' + device_id + '/messages/devicebound/#'

    # sas generator from https://github.com/bechynsky/AzureIoTDeviceClientPY/blob/master/DeviceClient.py
    def generate_sas_token(self, expiry=3600):
        ttl = int(time.time()) + expiry
        url_to_sign = urllib.parse.quote(self.endpoint, safe='') 
        sign_shared_access_key = "%s\n%d" % (url_to_sign, int(ttl))
        h = hmac.new(base64.b64decode(self.shared_access_key), msg = "{0}\n{1}".format(url_to_sign, ttl).encode('utf-8'),digestmod = 'sha256')
        signature = urllib.parse.quote(base64.b64encode(h.digest()), safe = '')
        return "SharedAccessSignature sr={0}&sig={1}&se={2}".format(url_to_sign, urllib.parse.quote(base64.b64encode(h.digest()), safe = ''), ttl)
        