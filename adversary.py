#!/usr/bin/env python3
'''Adversaries module to create threats for player'''

import pygame
import random
import time

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
    def __init__(self, image_path, width, height, window, player):
        self.counter = 0
        self.x = random.randrange(0, window.width-width)
        self.y = -height
        self._image = pygame.image.load(image_path)
        self.height = height
        self.width = width
        self._bullet_list = []
        self.dir = S
        self.window = window
        self.player = player
        self.alive = True
        self.delete = False

    def collision(self):
        for bullet in self.player.get_bullets():
            if self.x <= bullet[0] <= self.x + self.width and \
                        self.y <= bullet[1] <= self.y + self.height:
                self.alive = False
                self.player.del_bullet(bullet)

    def killed_player(self):
        '''Check if player is dead'''
        for bullet in self._bullet_list:
            if self.player.x + 3 <= bullet[0] <= self.player.x + \
                    self.player.width - 3 and self.player.y + 5 <= bullet[1] \
                    <= self.player.y + self.player.height - 5:
                return True

        return False


    def draw(self):
        '''Draw enemy to window'''
        # Check if alien died
        self.collision()
        # If not dead draw ship
        if self.alive:
            self.window.surf.blit(self._image, (self.x, self.y))
        elif not self._bullet_list:
            self.delete = True
        # Draw bullets
        for bullet in self._bullet_list:
            bullet[1] += 8
            if bullet[1] > self.window.height:
                self._bullet_list.remove(bullet)
            pygame.draw.circle(self.window.surf, RED, bullet, 4)


    def move(self):
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
                if 0 < self.x + options[self.dir][0] < \
                        self.window.width - self.width:
                    self.x += options[self.dir][0]
                if 0 < self.y + options[self.dir][1] < \
                        self.window.height - self.height:
                    self.y += options[self.dir][1]

    def shoot(self):
        self._bullet_list.append([int(self.x), int(self.y)])

    def reset(self):
        self.counter = 0
        self.x = random.randrange(0, self.window.width-self.width)
        self.y = -self.height
        self._bullet_list = []
        self.dir = S
        self.alive = True
        self.delete = False



class EnemyGenerator(object):
    def __init__(self, window, player):
        self.enemies = {}
        self.window = window
        self.player = player

    def init(self):
        self.reference = int(time.time())
        self.generated = False
        self.current_key = 0
        self.enemies = {}

    def update(self, score):
        if self.reference == int(time.time()) - 5 and not self.generated:
            self.generated = True
            self.reference = int(time.time())
            # Add difficulty based on level
            for index in range(0, min(score//10 + 1, 3)):
                self.current_key += 1
                self.enemies[self.current_key] = Enemy('sprites/alien_1.png',
                        34, 45, self.window, self.player)

        elif self.reference != int(time.time()) and self.generated:
            self.generated = False



