import time
import sys
import json
import logging
from socketIO_client_0_5_6 import SocketIO, LoggingNamespace

logging.basicConfig(level=logging.DEBUG)

def on_request(data):
    message = json.dumps(data)
    logging.info('on_request:')
    print(message)

def on_message(data):
    message = json.dumps(data)
    logging.info('on_message:%s', message)

def on_connect():
    request_message = {"symbolList":{"marketDepthTop":[{"symbolId":"btccny","pushType":"pushLong"}]},"version":1,"msgType":"reqMsgSubscribe"}
    socketIO.emit('request', request_message)

with SocketIO('hq.huobi.com', 80, LoggingNamespace) as socketIO:
    socketIO.on('connect', on_connect)
    socketIO.on('request', on_request)
    socketIO.on('message', on_message)

    socketIO.wait()
    

