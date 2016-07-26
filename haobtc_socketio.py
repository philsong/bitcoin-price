import time
import sys
import json
import logging
from socketIO_client import SocketIO, LoggingNamespace

logging.basicConfig(level=logging.INFO)

def on_request(data):
    message = json.dumps(data)
    logging.info('on_request:')
    print(message)

def on_message(data):
    message = json.dumps(data)
    logging.info('on_message:')
    print(message)

def on_connect():
    print('[Connected]')

    socketIO.emit('land', {'app': 'haobtcnotify', 'events':['depth']});

with SocketIO('app.haobtc.com', 80, LoggingNamespace) as socketIO:
    socketIO.on('connect', on_connect)
    socketIO.on('request', on_request)
    socketIO.on('message', on_message)

    socketIO.wait()
    

