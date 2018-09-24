import pygame

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
    def check(self):
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
            pygame.draw.rect(self.screen, self.active_color, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(self.screen, self.idle_color, (self.x, self.y, self.w, self.h))


