import time
import sys
import json
import logging
from socketIO_client_0_5_6 import SocketIO, LoggingNamespace
import tentacle
import utils

logging.basicConfig(level=logging.INFO)

def on_request(data):
    message = json.dumps(data)
    logging.debug('on_request:')
    logging.debug(message)

def on_message(data):
    payload = data['payload']

    depth = {}
    depth['bids'] = []
    depth['asks'] = []

    for index in range(len(payload['bidAmount'])):
        amount = payload['bidAmount'][index]
        price = payload['bidPrice'][index]
        bid = [price,amount]
        depth['bids'].append(bid)

    for index in range(len(payload['askAmount'])):
        amount = payload['askAmount'][index]
        price = payload['askPrice'][index]
        ask = [price,amount]
        depth['asks'].append(ask)
    
    depth = utils.sort_depth(depth)
    depth['timestamp'] = (payload['time'])
    depth['market'] = 'huobi'

    utils.pub_depth('depth_huobi', depth)

def on_connect():
    logging.debug('[Connected]')
    request_message = {"symbolList":{"marketDepthTop":[{"symbolId":"btccny","pushType":"pushLong"}]},"version":1,"msgType":"reqMsgSubscribe"}
    socketIO.emit('request', request_message)

if __name__ == "__main__":
    with SocketIO('hq.huobi.com', 80) as socketIO:
        socketIO.on('connect', on_connect)
        socketIO.on('request', on_request)
        socketIO.on('message', on_message)

        socketIO.wait()
    


