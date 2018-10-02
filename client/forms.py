import pygame

colors = {
    'white' : (255, 255, 255),
    'black' : (0, 0, 0),
    'gray'  : (150, 150, 150),
    'red'   : (255, 0, 0),
    'green' : (0, 255, 0),
    'blue'  : (0, 0, 255)
}

'''
Class representing a button. Ensures that a button press will call
action function exactly once per click.

'''
class Button():
    def __init__(self, screen, x, y, w, h, idle_color, active_color, text, action=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.idle_color = idle_color
        self.active_color = active_color
        self.text = text
        self.action = action
        self.active = False

    # checks to see if the button is being clicked -- if so, do action
    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # button is active and click false
        if self.active and click[0] == 0:
            self.active = False

        # button is not active and click true
        elif not self.active \
                and click[0] == 1 \
                and self.x + self.w > mouse[0] > self.x \
                and self.y + self.h > mouse[1] > self.y:

            self.active = True
            if self.action is not None:
                self.action()

    # renders the button in the correct color
    def render(self):
        if self.active:
            pygame.draw.rect(self.screen, colors[self.active_color], (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(self.screen, colors[self.idle_color], (self.x, self.y, self.w, self.h))

        font = pygame.font.SysFont('Comic Sans MS', 16)
        textSurface = font.render(self.text, False, (0, 0, 0))
        self.screen.blit(textSurface, (self.x, self.y))

'''
Class representing a text box. Keeps track of all rending and selection information.
Text updates are passed via. pygame.event through update, the method checks for if the
text box was clicked and if key presses were observed.

'''
class InputBox:

    def __init__(self, screen, x, y, w, h, idle_color, active_color, char_limit, text=''):
        self.screen = screen
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont('Comic Sans MS', 16)
        self.idle_color = idle_color
        self.active_color = active_color
        self.char_limit = char_limit
        self.text = text
        self.active = False

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        # add character if needed
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.char_limit:
                    self.text += event.unicode

    def render(self):
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.rect.x+5, self.rect.y+5))

        if self.active:
            pygame.draw.rect(self.screen, colors[self.active_color], self.rect, 2)
        else:
            pygame.draw.rect(self.screen, colors[self.idle_color], self.rect, 2)

