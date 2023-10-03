import os
import sys
import json
import time
import regex
import asyncio
import requests
import websocket
import threading




path_to_configs = 'configs.txt'

# TOKEN = 'MzQ4Nzg5ODI0MDMyOTk3Mzc2.GtqHvu.tUh-waMo2DN4HmQ8F_uS48RR-IUIAH0Th_A-aA'

f = open(path_to_configs)
input_data = json.loads(f.read()) 


TOKEN = input_data['token']
CHANNEL_ID = input_data['channel_id']
TO = input_data['to']
RESPONSE = input_data['response']
URL = "https://discord.com/api/v9/channels/" + str(CHANNEL_ID) + "/messages"


headers = {
    'authorization': TOKEN
}

message = {
    'content': RESPONSE
}

count = int(input("Chand bar?"))

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)
    
def heartbeat(interval, ws):
    print('Heartbeat started')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")


ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = receive_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000

threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

payload = {
    'op': 2,
    "d": {
        'token': TOKEN,
        'properties': {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc"
        }
    }
}

send_json_request(ws, payload)

i = 0

while True:

    if i >= count:
        break

    event = receive_json_response(ws)

    try:
        if event['d']['channel_id'] == str(CHANNEL_ID):
            content = event['d']['content']
            if TO in content:
                print(content)
                response = requests.post(url=URL, headers=headers, data=message)
                i += 1
        op_code = event('op')
        if op_code == 11:
            print('Heartbeat received')
    except:
        pass



        # {'type': 0, 'tts': False, 'timestamp': '2023-10-02T11:02:42.825000+00:00', 'referenced_message': None, 'pinned': False, 'nonce': '1158358398597595136', 'mentions': [], 'mention_roles': [], 'mention_everyone': False, 'member': {'roles': [], 'premium_since': None, 'pending': False, 'nick': None, 'mute': False, 'joined_at': '2023-10-01T13:03:31.471000+00:00', 'flags': 0, 'deaf': False, 'communication_disabled_until': None, 'avatar': None}, 'id': '1158358395833823343', 'flags': 0, 'embeds': [], 'edited_timestamp': None, 'content': 'a', 'components': [], 'channel_id': '1158026411387392002', 'author': {'username': 'thejou', 'public_flags': 0, 'id': '348789824032997376', 'global_name': 'The Jou', 'discriminator': '0', 'avatar_decoration_data': None, 'avatar': '0974170cc95eb41f3c29fe6c41db2fff'}, 'attachments': [], 'guild_id': '1158026410544332852'}   