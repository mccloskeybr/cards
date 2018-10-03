import pygame
import json
import request
import frontend
import forms

GAME_WIDTH = 780
GAME_HEIGHT = 780
SCREEN = None
CLOCK = None

MAX_TICKS_PER_SECOND = 60

player_id = -1


'''
Contains main game loop

'''
def game_loop():
    global player_id, SCREEN, CLOCK

    buttons = [
            forms.Button(SCREEN, GAME_WIDTH/2 - 30, 100, 60, 30, 'red', 'green', 'Reset', request.reset),
    ]

    table = frontend.Table(SCREEN, player_id)

    quit = False
    while not quit:
        CLOCK.tick(MAX_TICKS_PER_SECOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        players_json = request.get_players_json()
        table_json = request.get_table_json()
        table.load_json(table_json, players_json)

        table.check()

        SCREEN.fill(forms.colors['black'])

        for button in buttons:
            button.update()
            button.render()

        table.render()

        pygame.display.flip()
    
    pygame.quit()



'''
initializes global variables. makes initial check in with server and registers
the current player if the server allows it.

'''
def init():
    global player_id, SCREEN, CLOCK

    pygame.init()
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
            if request.attempt_connect(server_name.text.encode('ascii').replace(' ', '_')) == True:
                # start the server if not active
                if (str(request.active()) != 'True'):
                    request.start()

                # request registration
                player_id = int(request.register(display_name.text))
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


'''
Run any shutdown code necesarry

'''
def shutdown():
    global player_id

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

if __name__ == '__main__':
    init()

    # surround in try/catch so it will unregister if something fails
    try:
        game_loop()
    except Exception as error:
        print error

    shutdown()


