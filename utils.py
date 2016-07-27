import logging

def sort(l, reverse=False):
    l.sort(key=lambda x: float(x[0]), reverse=reverse)
    return l

def sort_depth(depth):
    bids = sort(depth['bids'], True)
    asks = sort(depth['asks'], False)
    return {'asks': asks, 'bids': bids}

def sort_and_format(l, reverse=False):
    l.sort(key=lambda x: float(x[0]), reverse=reverse)
    r = []
    for i in l:
        r.append({'price': float(i[0]), 'amount': float(i[1])})
    return r

def format_depth(depth):
    bids = sort_and_format(depth['bids'], True)
    asks = sort_and_format(depth['asks'], False)
    return {'asks': asks, 'bids': bids}

def pub_depth(event, depth):
    logging.debug(depth)

    try:
    	import tentacle
        r = tentacle.push_message({'event': event, 'data': depth})
    except:
        logging.debug('error on pushing exchange orderbook', exc_info=True)
