import pygame
import request
import frontend

GAME_WIDTH = 780
GAME_HEIGHT = 780

MAX_TICKS_PER_SECOND = 60

player_id = -1



def draw_main_to_hand():
    return request.draw_main_to_hand(player_id)

'''
Contains main game loop

'''
def game_loop():
    global player_id

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
    clock = pygame.time.Clock()

    buttons = [
            frontend.Button(screen, 10, 20, 100, 40, 'red', 'green', 'Reset', request.reset),
            frontend.Button(screen, 10, 70, 100, 40, 'red', 'green', 'Shuffle', request.shuffle),
            frontend.Button(screen, 10, 120, 100, 40, 'red', 'green', 'MainToTable', request.draw_main_to_table),
            frontend.Button(screen, 10, 170, 100, 40, 'red', 'green', 'MainToHand', draw_main_to_hand)
    ]

    table = frontend.Table(screen, player_id)

    quit = False
    while not quit:
        clock.tick(MAX_TICKS_PER_SECOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        table.update(request.get_table_json())

        screen.fill(frontend.color['black'])

        for button in buttons:
            button.check()
            button.render()

        table.render()

        pygame.display.flip()
    
    pygame.quit()



'''
Run pre-game checks and register with main gameserv

'''
def init():
    global player_id

    # ensure server is running
    if request.healthcheck() != 'True':
        print 'Server not running. Aborting.'
        quit()

    # register new player with server
    while player_id == -1:
        player_id = int(request.register())
        print 'Waiting to register...'
    print 'Registered!'



'''
Run any shutdown code necesarry

'''
def shutdown():
    global player_id

    request.unregister(player_id)

if __name__ == '__main__':
    init()

    # surround in try/catch so it will unregister if something fails
    try:
        game_loop()
    except Exception as error:
        print error

    shutdown()


