#!/usr/bin/env python3

'''player module defining class required to construct and draw the player
ship as well as the bullets shot from it'''

import pygame

# RGB colour definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Direction defintions
UP = 1
DOWN = 2
LEFT = 4
RIGHT = 8


class Player(object):
    '''Player class that represents the space ship controlled by player'''
    def __init__(self, window, image_path, width, height):
        '''Initialises position, image and image dimensions'''
        self.x = (window.width - width)/ 2
        self.y = window.height - height
        self.window = window
        self._image = pygame.image.load(image_path)
        self.width = width
        self.height = height
        self._v_speed = 5
        self._h_speed = 10
        self._bullet_list = []
        self.ammo = 0


    def draw(self, ammo_font):
        '''Draws player on window'''
        self.window.surf.blit(self._image, (self.x, self.y))
        for bullet in self._bullet_list:
            bullet[1] -= 15
            if bullet[1] < 0:
                self._bullet_list.remove(bullet)
            pygame.draw.circle(self.window.surf, BLACK, bullet, 2)

        ## Draw ammo counter
        if self.ammo > 3:
            text = ammo_font.render('Ammo: {0}'.format(self.ammo//4), True,
                    WHITE)
        else:
            text = ammo_font.render('Ammo: 0', True, RED)
        self.window.surf.blit(text, [4, self.window.height - 20])

    def move(self, move):
        '''Moves the player'''
        if move % 2 == 1 and self.y > self.window.height / 2:
            self.y -= self._v_speed
        if move % 4 == 2 and self.y + self.height < self.window.height:
            self.y += self._v_speed
        if move % 8 > 3 and self.x > 0:
            self.x -= self._h_speed
        if move >= 8 and self.x + self.width < self.window.width:
            self.x += self._h_speed

    def update_ammo(self):
        self.ammo += 1

    def set_h_speed(val):
        self._h_speed = val

    def set_v_speed(val):
        self._v_speed = val

    def shoot(self):
        if self.ammo > 1:
            self.ammo -= 4
            self._bullet_list.append([int(self.x + self.width/2), int(self.y)])

    def get_bullets(self):
        return self._bullet_list

    def del_bullet(self, bullet):
        try:
            self._bullet_list.remove(bullet)
        except ValueError:
            pass

    def reset(self):
        self.ammo = 0
        self._bullet_list = []
        self.x = (self.window.width - self.width)/ 2
        self.y = self.window.height - self.height
