import urllib2

local_url = 'http://localhost:56785'
remote_url = 'not implemented'

url = local_url


def start():
    return urllib2.urlopen(url + '/api/start').read()

def shutdown():
    return urllib2.urlopen(url + '/api/shutdown').read()

def reset():
    return urllib2.urlopen(url + '/api/reset').read()

def healthcheck():
    return urllib2.urlopen(url + '/api/healthcheck').read()

def register():
    return urllib2.urlopen(url + '/api/register').read()

def unregister(id):
    return urllib2.urlopen(url + '/api/unregister/' + str(id)).read()

def shuffle():
    return urllib2.urlopen(url + '/api/shuffle').read()

def draw_main_to_table():
    return urllib2.urlopen(url + '/api/draw_main_to_table').read()

def draw_main_to_hand(index):
    return urllib2.urlopen(url + '/api/draw_main_to_hand/' + str(index)).read()

def draw_hand_to_table(hand_index, card_index):
    return urllib2.urlopen(url + '/api/draw_hand_to_table/' + str(hand_index) + '/' + str(card_index)).read()

def draw_table_to_hand(hand_index, card_index):
    return urllib2.urlopen(url + '/api/draw_table_to_hand/' + str(hand_index) + '/' + str(card_index)).read()

def get_table_json():
    return urllib2.urlopen(url + '/api/table').read()
