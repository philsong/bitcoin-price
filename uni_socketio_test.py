import time
import sys
import json
import logging
from socketIO_client import SocketIO, LoggingNamespace
import settings

logging.basicConfig(level=logging.INFO)

def on_message(data):
    message = json.dumps(data)
    logging.info('on_message:')
    print(message)

def on_connect():
    logging.debug('[Connected]')

    socketIO.emit('land', {'app': 'haobtcnotify', 'events':['depth_okcoin','depth_huobi','depth_haobtc']});

if __name__ == "__main__":
    with SocketIO(settings.HAOBTC_HOST, port=settings.HAOBTC_PORT, Namespace=LoggingNamespace) as socketIO:

        socketIO.on('connect', on_connect)
        socketIO.on('message', on_message)

        socketIO.wait()
    

