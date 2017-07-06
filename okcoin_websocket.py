import websocket
import time
import sys
import json
import hashlib
import zlib
import base64
import tentacle
import logging
import utils

sub_channel_name = 'ok_sub_spotcny_btc_depth_60'

def on_open(self):
    logging.debug('[Connected]')
    #subscribe okcoin.com spot depth
    self.send("{'event':'addChannel','channel':'%s','binary':'0'}" % sub_channel_name)
    
def on_message(self,evt):
    # data = inflate(evt) #data decompress
    # print(evt)
    data = evt

    data = json.loads(data)
    try:
        if data[0]['channel'] == 'addChannel':
            return
        if data[0]['channel'] == sub_channel_name:
            depth = data[0]['data']
    except Exception, e:
        return

    depth = utils.sort_depth(depth)
    depth['timestamp'] = int(data[0]['data']['timestamp'])
    depth['market'] = 'okcoin'

    utils.pub_depth('okcoin_depth', depth)

def inflate(data):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

def on_error(self,evt):
    logging.debug ('error: %s', evt)

def on_close(self):
    logging.debug ('DISCONNECT')

if __name__ == "__main__":
    url = "wss://real.okcoin.cn:10440/websocket/okcoinapi"     

    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = url
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
