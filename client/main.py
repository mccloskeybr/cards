import pygame
import json
import threading
import request
import frontend
import forms

GAME_WIDTH = 780
GAME_HEIGHT = 780
SCREEN = None
CLOCK = None
MAX_TICKS_PER_SECOND = 60

TABLE = None
player_id = -1

SERVER_THREAD = None
QUIT = False

'''
Regularly grabs server information and updates the shared table object.
Including this massively decreases visual lag associated with communicating with
the server, especially if it is remote (i.e. thru AWS)

'''
def communicate_server_loop():
    global TABLE, QUIT

    while QUIT == False:
        players_json = request.get_players_json()
        table_json = request.get_table_json()
        TABLE.load_json(table_json, players_json)

'''
Contains main game loop

'''
def game_loop():
    global player_id, SCREEN, CLOCKS, TABLE, SERVER_THREAD, QUIT

    buttons = [
            forms.Button(SCREEN, GAME_WIDTH/2 - 30, 100, 60, 30, 'red', 'green', 'Reset', request.reset),
    ]

    TABLE = frontend.Table(SCREEN, player_id)

    SERVER_THREAD = threading.Thread(target=communicate_server_loop).start()

    QUIT = False
    while QUIT == False:
        CLOCK.tick(MAX_TICKS_PER_SECOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT = True

        TABLE.update()

        SCREEN.fill(forms.colors['black'])

        TABLE.render()
        for button in buttons:
            button.update()
            button.render()

        pygame.display.flip()


'''
initializes global variables. makes initial check in with server and registers
the current player if the server allows it.

'''
def init():
    global player_id, SCREEN, CLOCK

    pygame.init()
    pygame.display.set_caption("Cards")
    pygame.font.init()

    SCREEN = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
    CLOCK = pygame.time.Clock()

    submit = forms.Button(SCREEN, 10, 20, 100, 40, 'red', 'green', 'Submit', None)
    display_name = forms.InputBox(SCREEN, 10, 70, 200, 30, 'red', 'green', 20, 'Name')
    server_name = forms.InputBox(SCREEN, 10, 110, 500, 30, 'red', 'green', 45, 'Server')

    accepted = False
    while not accepted:

        CLOCK.tick(MAX_TICKS_PER_SECOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            display_name.update(event)
            server_name.update(event)
        
        submit.update()

        if submit.active == True:
            submit.active = False
            # attempt to connect
            if request.attempt_connect(server_name.text.encode('ascii')) == True:
                # start the server if not active
                if (str(request.active()) != 'True'):
                    request.start()

                # request registration
                player_id = int(request.register(display_name.text.replace(' ', '_')))
                if player_id != -1:
                    accepted = True
                else:
                    server_name.text = 'Server full!'

            else:
                print server_name.text
                server_name.text = 'Invalid server'

        SCREEN.fill(forms.colors['black'])

        display_name.render()
        server_name.render()
        submit.render()

        pygame.display.flip()

    # start communicating with the server (stops automatically via. QUIT)
    SERVER_THREAD = threading.Thread(target=communicate_server_loop).start()

'''
Run any shutdown code necesarry

'''
def shutdown():
    global player_id, SERVER_THREAD

    # unregister player
    request.unregister(player_id)

    # shutdown server if no players
    players = json.loads(request.get_players_json())['players']
    shutdown = True
    for player in players:
        if player['name'] != 'null':
            shutdown = False
            break
    if shutdown:
        request.shutdown()

    pygame.quit()

if __name__ == '__main__':
    init()

    # surround in try/catch so it will unregister if something fails
    try:
        game_loop()
    except Exception as error:
        print error

    shutdown()


