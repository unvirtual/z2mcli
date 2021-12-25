import json
import paho.mqtt.client as mqtt

class Z2MClient:
    def __init__(self, config):
        self.client = mqtt.Client()
        self.client.connect(config['broker_host'], config['broker_port'], 60)
        self.config = config

        self.BRIDGE_REQUEST_TOPIC= self.config["base_topic"] + "/bridge/request"
        self.RESET_TOPIC = self.BRIDGE_REQUEST_TOPIC + "/reset"
        self.DEVICE_RENAME_TOPIC = self.BRIDGE_REQUEST_TOPIC + "/device/rename"
        self.DEVICE_REMOVE_TOPIC = self.BRIDGE_REQUEST_TOPIC + "/device/remove"

    @classmethod
    def rename_msg(cls, from_id, to_id, rename_in_homeassistant):
        msg = {}
        if from_id != None:
            msg["from"] = from_id
        else:
            msg["last"] = True
        msg["to"] = to_id
        if rename_in_homeassistant:
            msg["homeassistant_rename"] = True
        return json.dumps(msg)

    def reset(self):
        self.client.publish(self.RESET_TOPIC, "")

    def rename(self, src, dst, rename_in_homeassistant=False):
        self.client.publish(self.DEVICE_RENAME_TOPIC, Z2MClient.rename_msg(src, dst, rename_in_homeassistant))

    def rename_last(self, dst, rename_in_homeassistant=False):
        self.client.publish(self.DEVICE_RENAME_TOPIC, Z2MClient.rename_msg(None, dst, rename_in_homeassistant))

    def remove(self, id, force=False):
        msg = {"id": id}
        if force:
            msg["force"] = True
        self.client.publish(self.DEVICE_REMOVE_TOPIC, json.dumps(msg))