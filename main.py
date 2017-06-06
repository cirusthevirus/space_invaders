#!/usr/bin/env python3

'''Main game loop. Imports player and adversary classes to construct ships.
'''

import pygame
import time
import window
import player
import adversary

# RGB colour definitions
WHITE = (255, 255, 255)

# Frames per second definition
FPS = 60

# Initialise pygame window
window = window.Window(500, 800)
window.set_title('Space Invaders')
window.set_background('sprites/space.jpeg')

# Other constants (after pygame init called in Window.__init__)
SCORE_FONT = pygame.font.Font('freesansbold.ttf', 20)
AMMO_FONT = pygame.font.Font('freesansbold.ttf', 15)

# Initialise clock
clock = pygame.time.Clock()

# Initialise player and adversaries
player1 = player.Player(window, 'sprites/player_icon.png', 26, 60)
aliens = adversary.EnemyGenerator(window, player1)

def game_over():
    small_font = pygame.font.Font('freesansbold.ttf', 15)
    large_font = pygame.font.Font('freesansbold.ttf', 70)

    title_text_surf, title_text_rect = make_text_obj('Game Over!', large_font)
    title_text_rect.center = window.width / 2, window.height / 2
    window.surf.blit(title_text_surf, title_text_rect)

    key_text_surf, key_text_rect = make_text_obj("Press 'x' to continue",
                                                 small_font)
    key_text_rect.center = window.width / 2, window.height / 2 + 100
    window.surf.blit(key_text_surf, key_text_rect)

    pygame.display.update()
    time.sleep(0.5)

    while replay_or_quit() == None:
        clock.tick()

    player1.reset()
    for enemy in aliens.enemies.values():
        enemy.reset()
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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
    return None

def make_text_obj(text, font):
    text_surf = font.render(text, True, WHITE)
    return text_surf, text_surf.get_rect()

def draw_score(score):
    text = SCORE_FONT.render('Score: {0}'.format(score), True, WHITE)
    window.surf.blit(text, [0, 0])


def main():
    # Initialise score enemies and player movement
    move = 0
    score = 0
    aliens.init()
    bullet_speed = 4
    shoot_rate = 12
    while True:
        bullet_speed, shoot_rate = aliens.update(score)
        dead_aliens = []
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
        else:
            player1.update_ammo()



        player1.move(move)
        for enemy in aliens.enemies.values():
            enemy.move(shoot_rate)


        # Main loop
        window.draw()
        player1.draw(AMMO_FONT)

        for key, enemy in aliens.enemies.items():
            if enemy.delete:
                dead_aliens.append(key)

        for key in dead_aliens:
            aliens.enemies.pop(key, None)
            score += 1
            if key == 'boss':
                score += 2

        for enemy in aliens.enemies.values():
            enemy.draw(bullet_speed)

        draw_score(score)

        for enemy in aliens.enemies.values():
            if enemy.killed_player():
                game_over()


        pygame.display.update()
        clock.tick(FPS)

main()
pygame.quit()
quit()
