import time
import sys
import json
import logging
from socketIO_client import SocketIO, LoggingNamespace
import utils

logging.basicConfig(level=logging.INFO)

def on_message(data):
    data = data.decode('utf8')
    if data[0] != '2':
        return

    data = json.loads(data[1:])

    depth = {}
    depth['bids'] = []
    depth['asks'] = []

    for bid in data[1]['bid']:
        bid = [bid['price'],bid['remainsize']]
        depth['bids'].append(bid)

    for ask in data[1]['ask']:
        ask = [ask['price'],ask['remainsize']]
        depth['asks'].append(ask)
    
    depth = utils.sort_depth(depth)
    depth['timestamp'] = int(1000*time.time())
    depth['market'] = 'haobtc'

    utils.pub_depth('depth_haobtc', depth)

def on_connect():
    logging.debug('[Connected]')

    socketIO.emit('land', {'app': 'haobtcnotify', 'events':['orderbook']});

if __name__ == "__main__":
    with SocketIO('http://app.haobtc.com') as socketIO:

        socketIO.on('connect', on_connect)
        socketIO.on('message', on_message)

        socketIO.wait()
    