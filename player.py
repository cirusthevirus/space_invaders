#!/usr/bin/env python3

'''player module defining class required to construct and draw the player
ship as well as the bullets shot from it'''

import pygame

# RGB colour definitions
BLACK = (0, 0, 0)

# Direction defintions
UP = 1
DOWN = 2
LEFT = 4
RIGHT = 8


class Player(object):
    '''Player class that represents the space ship controlled by player'''
    def __init__(self, x, y, image_path, width, height):
        '''Initialises position, image and image dimensions'''
        self.x = x
        self._ini_x = x
        self.y = y
        self._ini_y = y
        self._image = pygame.image.load(image_path)
        self.width = width
        self.height = height
        self._v_speed = 5
        self._h_speed = 10
        self._bullet_list = []


    def draw(self, window):
        '''Draws player on window'''
        window.blit(self._image, (self.x, self.y))
        for bullet in self._bullet_list:
            bullet[1] -= 10
            if bullet[1] < 0:
                self._bullet_list.remove(bullet)
            pygame.draw.circle(window, BLACK, bullet, 2)

    def move(self, move, width_lim, height_lim):
        '''Moves the player'''
        if move % 2 == 1 and self.y > height_lim / 2:
            self.y -= self._v_speed
        if move % 4 == 2 and self.y + self.height < height_lim:
            self.y += self._v_speed
        if move % 8 > 3 and self.x > 0:
            self.x -= self._h_speed
        if move >= 8 and self.x + self.width < width_lim:
            self.x += self._h_speed

    def set_h_speed(val):
        self._h_speed = val

    def set_v_speed(val):
        self._v_speed = val

    def shoot(self):
        self._bullet_list.append([int(self.x), int(self.y)])

    def get_bullets(self):
        return self._bullet_list

    def del_bullet(self, bullet):
        try:
            self._bullet_list.remove(bullet)
        except ValueError:
            pass

    def reset(self):
        self._bullet_list = []
        self.x = self._ini_x
        self.y = self._ini_y
