import urllib2

URL = ''
URL = 'http://ec2-54-173-205-157.compute-1.amazonaws.com'
URL = 'http://localhost:5757'

def attempt_connect(url):
    global URL
    try:
        #URL = 'http://' + url
        urllib2.urlopen(URL + '/api/healthcheck').read()
        return True
    except Exception as error:
        print error
        return False

def start():
    return urllib2.urlopen(URL + '/api/start').read()

def shutdown():
    return urllib2.urlopen(URL + '/api/shutdown').read()

def reset():
    return urllib2.urlopen(URL + '/api/reset').read()

def healthcheck():
    return urllib2.urlopen(URL + '/api/healthcheck').read()

def register(name):
    return urllib2.urlopen(URL + '/api/register/' + name).read()

def unregister(id):
    return urllib2.urlopen(URL + '/api/unregister/' + str(id)).read()

def shuffle():
    return urllib2.urlopen(URL + '/api/shuffle').read()

def draw_main_to_table():
    return urllib2.urlopen(URL + '/api/draw_main_to_table').read()

def draw_main_to_hand(index):
    return urllib2.urlopen(URL + '/api/draw_main_to_hand/' + str(index)).read()

def draw_hand_to_table(hand_index, card_index):
    return urllib2.urlopen(URL + '/api/draw_hand_to_table/' + str(hand_index) + '/' + str(card_index)).read()

def draw_table_to_hand(hand_index, card_index):
    return urllib2.urlopen(URL + '/api/draw_table_to_hand/' + str(hand_index) + '/' + str(card_index)).read()

def get_table_json():
    return urllib2.urlopen(URL + '/api/table').read()

def get_display_names_json():
    return urllib2.urlopen(URL + '/api/displaynames').read()
