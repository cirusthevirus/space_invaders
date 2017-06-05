#!/usr/bin/env python3
'''Adversaries module to create threats for player'''

import pygame
import player
import random

# RGB colour definitions
RED = (255, 0, 0)

N = 0
E = 1
S = 2
W = 3
SE = 4
SW = 5
NW = 6
NE = 7

options = {N: (0, -3),
           E: (7, 0),
           S: (0, 3),
           W: (-7, 0),
           SE: (7, 3),
           SW: (-7, 3),
           NW: (-7, -3),
           NE: (7, -3)}


class Enemy(object):
    '''Single enemy space ship instance'''
    def __init__(self, image_path, width, height, width_lim, height_lim, pl):
        self.counter = 0
        self.x = random.randrange(0, width_lim-width)
        self.y = -height
        self._image = pygame.image.load(image_path)
        self.height = height
        self.width = width
        self._bullet_list = []
        self.dir = S
        self.window_h_lim = height_lim
        self.window_w_lim = width_lim
        self.player = pl
        self.alive = True
        self.delete = False

    def collision(self):
        for bullet in self.player.get_bullets():
            if self.x <= bullet[0] <= self.x + self.width and \
                        self.y <= bullet[1] <= self.y + self.height:
                self.alive = False
                self.player.del_bullet(bullet)

        # Check if player is dead
        for bullet in self._bullet_list:
            if self.player.x <= bullet[0] <= self.player.x + self.player.width\
                    and self.player.y <= bullet[1] <= self.player.y +\
                    self.player.height:
                return True

        return False


    def draw(self, window):
        '''Draw enemy to window'''
        # If not dead draw ship
        if self.alive:
            window.blit(self._image, (self.x, self.y))
        elif not self._bullet_list:
            self.delete = True
        # Draw bullets
        for bullet in self._bullet_list:
            bullet[1] += 8
            if bullet[1] > self.window_h_lim:
                self._bullet_list.remove(bullet)
            pygame.draw.circle(window, RED, bullet, 4)
        # Check for collisions
        return self.collision()

    def move(self, width_lim, height_lim):
        '''Moves spaceship randomly'''
        # If alive shoot every 8 frames
        if self.alive:
            self.counter += 1
            if self.counter > 8:
                self.counter = 0
                self.shoot()

            direction = random.randrange(0, 99)
            if direction < 2:
                self.dir = (self.dir - 2) % 8   # 180 degree change
            elif direction < 6:
                self.dir = (self.dir - 1) % 8   # likely -90 degree change
            elif direction < 10:
                self.dir = (self.dir + 1) % 8   # likely +90  degree change
            elif direction < 12:
                self.dir = (self.dir + 3) % 8   # quasi random change
            elif direction < 14:
                self.dir = (self.dir - 3) % 8   # other quasi random change

            # Move down if above window
            if self.y < 0:
                self.y += options[S][1]
            else:      # Perform movement if in window
                if 0 < self.x + options[self.dir][0] < width_lim-self.width:
                    self.x += options[self.dir][0]
                if 0 < self.y + options[self.dir][1] < height_lim-self.height:
                    self.y += options[self.dir][1]

    def shoot(self):
        self._bullet_list.append([int(self.x), int(self.y)])

    def reset(self):
        self.counter = 0
        self.x = random.randrange(0, self.window_w_lim-self.width)
        self.y = -self.height
        self._bullet_list = []
        self.dir = S
        self.alive = True
        self.delete = False

