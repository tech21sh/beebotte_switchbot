# coding: utf-8
import paho.mqtt.client as mqtt
import json
import requests
import binascii
from bluepy.btle import Peripheral

# beebotte
TOKEN         = "xxxxxxxxxxxx"
HOSTNAME      = "mqtt.beebotte.com"
PORT          = 8883
TOPIC         = "[�`�����l����]/[���\�[�X��]"
CACERT        = "mqtt.beebotte.com.pem"

# IFTTT
RES_IFTTT_URL = "https://maker.ifttt.com/trigger/[�C�x���g��]/with/key/[�V�[�N���b�g�L�[]"

# switchbot
MAC_ADDR      = "[switchbot��MAC�A�h���X]"

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))["data"]
    if data == "FillTheBath":
        # switchbot�N��
        trigger_switchbot()
        res = "FillTheBathCompleted!!!"
    elif data == "Alive":
        # �������Ȃ��i���b�Z�[�W�ʒm�̂݁j
        res = "KeepAlive!!!"
    else:
        res = "NoCommands"
    print(res)
    request_webhooks(res)

def request_webhooks(msg):
    # IFTTT�o�R�̊������b�Z�[�W��ԑ�
    url = RES_IFTTT_URL
    payload = {'value1': msg}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)    

def trigger_switchbot():
    p = Peripheral(MAC_ADDR, "random")
    hand_service = p.getServiceByUUID("cba20d00-224d-11e6-9fb8-0002a5d5c51b")
    hand = hand_service.getCharacteristics("cba20002-224d-11e6-9fb8-0002a5d5c51b")[0]
    hand.write(binascii.a2b_hex("570100"))
    p.disconnect()

client = mqtt.Client()
client.username_pw_set("token:%s"%TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(CACERT)
client.connect(HOSTNAME, port=PORT, keepalive=60)
client.loop_forever()