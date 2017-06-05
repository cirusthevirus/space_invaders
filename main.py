#!/usr/bin/env python3

'''Main game loop. Imports player and adversary classes to construct ships.
'''

import pygame
import time
import player
import adversary

# RGB colour definitions
WHITE = (255, 255, 255)

# Frames per second definition
FPS = 60

# Initialise pygame
pygame.init()

# Set window
window_w = 500
window_h = 800
window = pygame.display.set_mode((window_w, window_h))
background = pygame.image.load('sprites/space.jpeg')
pygame.display.set_caption('Space Invaders')
# Time tracker
clock = pygame.time.Clock()

player1 = player.Player(window_w/2 - 13, window_h - 70,
                        'sprites/player_icon.png',
                        26, 60)

enemy1 = adversary.Enemy('sprites/alien_1.png', 34, 45,
                         window_w, window_h, player1)

def game_over():
    small_font = pygame.font.Font('freesansbold.ttf', 15)
    large_font = pygame.font.Font('freesansbold.ttf', 70)

    title_text_surf, title_text_rect = make_text_obj('Game Over!', large_font)
    title_text_rect.center = window_w / 2, window_h / 2
    window.blit(title_text_surf, title_text_rect)

    key_text_surf, key_text_rect = make_text_obj("Press 'x' to continue",                                         small_font)
    key_text_rect.center = window_w / 2, window_h / 2 + 100
    window.blit(key_text_surf, key_text_rect)

    pygame.display.update()
    time.sleep(0.5)

    while replay_or_quit() == None:
        clock.tick()

    player1.reset()
    enemy1.reset()
    main()

def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                pygame.event.clear()
                return True
    return None

def make_text_obj(text, font):
    text_surf = font.render(text, True, WHITE)
    return text_surf, text_surf.get_rect()


def main():
    move = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move += player.UP
                if event.key == pygame.K_DOWN:
                    move += player.DOWN
                if event.key == pygame.K_LEFT:
                    move += player.LEFT
                if event.key == pygame.K_RIGHT:
                    move += player.RIGHT

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    move -= player.UP
                if event.key == pygame.K_DOWN:
                    move -= player.DOWN
                if event.key == pygame.K_LEFT:
                    move -= player.LEFT
                if event.key == pygame.K_RIGHT:
                    move -= player.RIGHT

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE]:
            player1.shoot()


        player1.move(move, window_w, window_h)
        enemy1.move(window_w, window_h)


        # Main loop
        window.blit(background, (0, 0))
        player1.draw(window)
        if not enemy1.delete:
            if enemy1.draw(window):
                game_over()

        pygame.display.update()
        clock.tick(FPS)

main()
pygame.quit()
quit()
