#!/usr/bin/env python
# -*- coding:utf-8 -*-
from time_made_home import *
from player import *
from manager import *
from levels import *


class Survival(object):
    def __init__(self, main):
        self.width = main.width
        self.height = main.height

        self.window = main.window
        self.background = main.background

        self.game_images = main.game_images
        self.obstacles_images = main.obstacles_images
        self.character_images = main.character_images

        self.is_mouse_button_down = main.is_mouse_button_down

        self.hud_font = main.hud_font
        self.welcome_font0 = main.welcome_font0
        self.welcome_font1 = main.welcome_font1
        self.final_score_font = main.final_score_font

        self.button_accueil = main.button_accueil
        self.button_next_level = main.button_next_level

        self.time = Times()
        self.clock = pygame.time.Clock()

        self.frameRate = 0
        self.frameCount = 0

        self.victims = 0
        self.run = None
        self.click_pos_x = None
        self.click_pos_y = None
        self.enemy_hit_list = None
        self.obstacles_collided = None

        self.is_game_over = False

        self.create_player()

        self.levels = Levels(self)
        self.levels.init_survival_level()

        self.main()

    def text_blit(self, font, text, text_color, pos):
        text_to_blit = font.render(text, 1, text_color)
        text_to_blit_pos = text_to_blit.get_rect(centerx=pos[0], centery=pos[1])
        self.background.blit(text_to_blit, text_to_blit_pos)

    def create_player(self):
        """Creation du joueur"""
        print('[*] Player Init')
        self.player_sprite = pygame.sprite.Group()
        self.player = Player('player', self.character_images['player'], 512, 354, self.width, self.height)
        self.time.add_rebour('player')
        self.player_sprite.add(self.player)
        print('     - Ok')

    def click_motion(self):
        """Gestion du déplacement du joueur au click"""
        if self.click_pos_x == self.player.rect.x:
            self.player.moveX = 0
            self.click_pos_x = None
        if self.click_pos_y == self.player.rect.y:
            self.player.moveY = 0
            self.click_pos_y = None

        if self.click_pos_x is not None:
            if self.click_pos_x < self.player.rect.x:
                self.player.action = 'left'
                self.player.move_left()
            elif self.click_pos_x > self.player.rect.x:
                self.player.action = 'right'
                self.player.move_right()
        if self.click_pos_y is not None:
            if self.click_pos_y < self.player.rect.y:
                self.player.action = 'up'
                self.player.move_up()
            elif self.click_pos_y > self.player.rect.y:
                self.player.action = 'down'
                self.player.move_down()

        if self.click_pos_x is None and self.click_pos_y is None:
            self.player.action = ''

    def init_game_over(self):
        print('[*] Init Game Over')
        # Pose l'image
        self.background.blit(self.game_images['game_over_image'], (self.width/6.6, self.height/3.5))
        self.background.blit(self.game_images['skull_image'], (self.width/3.15, self.height/2.1))
        self.background.blit(self.game_images['skull_image'], (self.width/1.55, self.height/2.1))

        # Définit et pose les texts
        self.text_blit(self.final_score_font, "Vous etes definitivement",
                       (255, 255, 255), (self.width/2, self.height/2.4))

        self.text_blit(self.welcome_font1, "M.O.R.T",
                       (255, 255, 255), (self.width/2, self.height/2.1))

        self.text_blit(self.final_score_font, 'Score final: ' + str(self.player.final_score),
                       (255, 255, 255), (self.width/2, self.height/1.8))

        self.text_blit(self.final_score_font, 'Accueil',
                       (255, 255, 255), (self.width/2, self.height/1.435))

        # Pose le bouton retour accueil
        self.button_accueil = pygame.draw.rect(self.window, [0, 0, 0],
                                               [self.background.get_width()/2.35, self.height/1.5, 145, 45])

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        print('     - Ok')

    def display_game_over(self, end_type):
        self.is_game_over = True

        if end_type == 'game_over':
            self.init_game_over()

        while self.is_game_over:
            self.display_hud()
            mouse_xy = pygame.mouse.get_pos()
            is_accueil = self.button_accueil.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and is_accueil:
                    self.is_game_over = False
                    self.end_game()

            pygame.display.flip()

    def end_game(self):
        print('[*] Start New Game')
        self.run = False

    def display_hud(self):
        """Affichage Tête Haute (score - temps.....)"""
        current_lvl = self.hud_font.render('%s %s' % ('Mort: ', self.victims), True, (0, 0, 0))  # a remplacer par le nm d'eneme tués
        score = self.hud_font.render('%s' % self.player.score, True, (0, 0, 0))  # player.score
        time = self.hud_font.render('%s:%s:%s' % (self.time.chronos['survival'].Time[0],
                                                  self.time.chronos['survival'].Time[1],
                                                  self.time.chronos['survival'].Time[2]), True, (0, 0, 0))  # time

        self.window.blit(current_lvl, (50, 14))
        self.window.blit(score, (492, 14))
        self.window.blit(time, (878, 14))

    def main(self):
        print('[*] Launch Campagne')
        self.run = True
        self.levels.current_level.start()

        print('[*] Start')
        while self.run:
            mouse_xy = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_mouse_button_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_mouse_button_down = False

            # -------------------------Update--------------------------

            if self.is_mouse_button_down:
                self.click_pos_x = mouse_xy[0] - self.player.width / 2
                self.click_pos_y = mouse_xy[1] - self.player.height / 2

            self.click_motion()
            self.time.update()
            self.player.update(self.levels.current_level.obstacles.objects_list)
            self.levels.current_level.update(self.levels.current_level.obstacles.objects_list)

            if self.player.dying:
                self.display_game_over('game_over')

            # ------------------------Display------------------------

            self.window.blit(self.background, (0, 0))
            self.display_hud()
            self.levels.current_level.pnj.draw()

            self.levels.current_level.obstacles.objects_list.draw(self.window)
            # Si le joueur mange, ne l'affiche pas
            if not self.player.is_feeding:
                self.player_sprite.draw(self.window)

            pygame.display.flip()
            self.clock.tick(100)













