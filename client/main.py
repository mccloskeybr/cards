import pygame
from frontend import Button
import wrapper

GAME_WIDTH = 780
GAME_HEIGHT = 780

MAX_TICKS_PER_SECOND = 60

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

    table_wrapper = wrapper.TableWrapperClass(1)

    buttons = [
            Button(screen, 50, 50, 100, 50, color['red'], color['green'], "", table_wrapper.print_main),
            Button(screen, 50, 120, 100, 50, color['red'], color['green'], "", table_wrapper.shuffle_main_deck)
    ]

    quit = False
    while not quit:
        clock.tick(MAX_TICKS_PER_SECOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        screen.fill(color['black'])

        for button in buttons:
            button.check()
            button.render()

        pygame.display.flip()

    pygame.quit()



if __name__ == '__main__':
    game_loop()


