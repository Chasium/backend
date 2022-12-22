"""
后端所有的Websocket API。
具体的API由APIGen生成。
"""
from flask_socketio import SocketIO
from engineio.payload import Payload

Payload.max_decode_packets = 100

ws_api = SocketIO()


from apigen.ws_api import *