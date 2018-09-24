import pygame
import frontend
import wrapper

GAME_WIDTH = 500
GAME_HEIGHT = 500

color = {
    'white' : (255, 255, 255),
    'black' : (0, 0, 0),
    'red'   : (255, 0, 0),
    'blue'  : (0, 0, 255),
    'green' : (0, 255, 0),
    'purple': (255, 0, 255),
    'orange': (255, 127, 0)
}

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
    clock = pygame.time.Clock()
    max_ticks_per_second = 60

    table_wrapper = wrapper.TableWrapperClass(1)

    buttons = []
    buttons.append(frontend.Button(screen, 50, 50, 100, 50, color['red'], color['green'], "", table_wrapper.print_main))
    buttons.append(frontend.Button(screen, 50, 120, 100, 50, color['red'], color['green'], "", table_wrapper.shuffle_main_deck))

    quit = False
    while not quit:
        clock.tick(max_ticks_per_second)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        screen.fill(color['black'])

        for button in buttons:
            button.check()
            button.render()

        pygame.display.flip()

    pygame.quit()

game_loop()


