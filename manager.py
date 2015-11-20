#!/usr/bin/env python
# -*- coding:utf-8 -*-
from character import *
import constants


class PNJ(object):
    def __init__(self, main, start_enemy_list, level):
        self.enemy_list = pygame.sprite.Group()
        self.zombie_list = pygame.sprite.Group()
        self.feeding_zombie_list = pygame.sprite.Group()

        self.main = main
        self.level = level
        self.init_pnj(start_enemy_list)

    def init_pnj(self, enemy_data):
        """Initialise les Personnages Non Joueur"""
        print('     - PNJ Init in Progress')
        pnj_num = 0  # compteur pour différencier les pnj
        for pos in enemy_data.keys():
            new_enemy = Humain(self.main, enemy_data[pos], pos, pnj_num)
            self.enemy_list.add(new_enemy)
            pnj_num += 1
            print('.'),

    def add_zombie(self, main, name, pos, num):
        """Ajoute un nouveau zombie a la liste des zombie en 'vie' """
        print('[*] ' + name + ' Going Zombie')
        zombie = Zombie(main, name, pos, num)
        self.zombie_list.add(zombie)
        print('[*] New Zombie')

    def remove_zombie(self):
        """Supprime tout les zombie restant en fin de niveau"""
        print('[*] Remove Remaining Zombies')
        for zombie in self.zombie_list:
            self.zombie_list.remove(zombie)
        print('     - Ok')

    def pnj_collide(self):
        """
        Tests de collisions
        rectangle-rectangle puis au pixel près
        """

        # test circle collision
        for enemy in self.enemy_list:
            if pygame.sprite.collide_circle(self.main.player, enemy):
                print('[*] ' + enemy.name + str(enemy.num) + ' Collide Circle')

        # Collision avec le joueur
        if not self.main.player.is_feeding:
            enemy_hit_list = pygame.sprite.spritecollide(self.main.player, self.enemy_list, False)
            for enemy in enemy_hit_list:
                if pygame.sprite.collide_mask(self.main.player, enemy) is not None:
                    if not enemy.is_under_attack and not self.main.player.is_feeding:
                        print('[*] Mask Collide - Player')
                        enemy.under_attack(self.main.player)
                        self.main.player.is_feeding = True

        # Collsision avec les autres zombies
        for zombie in self.zombie_list:
            if not zombie.is_feeding:
                enemy_hit_list = pygame.sprite.spritecollide(zombie, self.enemy_list, False)
                for enemy in enemy_hit_list:
                    if pygame.sprite.collide_mask(zombie, enemy) is not None:
                        if not enemy.is_under_attack and not zombie.is_feeding:
                            print('[*] Mask Collide - Zombie')
                            enemy.under_attack(zombie)
                            zombie.is_feeding = True

    def update(self, obsctacles_list):
        """met les pnj a jour"""
        for enemy in self.enemy_list:
            if not enemy.is_alive:
                print('[*] Remove Humain')
                self.enemy_list.remove(enemy)

        for zombie in self.zombie_list:
            if not zombie.is_alive:
                print('[*] Remove Zombie')
                self.zombie_list.remove(zombie)

        if len(self.enemy_list) == 0 and self.level.is_started:
            print('[*] Change Lvl => True')
            self.level.is_change_level = True

        self.pnj_collide()
        self.enemy_list.update(obsctacles_list)
        self.zombie_list.update(obsctacles_list)

    def draw(self):
        """dessine les pnj"""
        self.enemy_list.draw(self.main.window)

        # Ne pas afficher les zombie 'ia' qui se baffrent
        if len(self.zombie_list) != 0:
            for zombie in self.zombie_list:
                if zombie.is_feeding:
                    self.feeding_zombie_list.add(zombie)
                    self.zombie_list.remove(zombie)

            self.zombie_list.draw(self.main.window)

            for zombie in self.feeding_zombie_list:
                self.zombie_list.add(zombie)
                self.feeding_zombie_list.remove(zombie)


class Obstacles(object):
    def __init__(self, main):
        """
        Obstacle initialiser avec les position des objets sur la feuille de sprite
        Remplacés par [image, rect] correspondantent juste en dessous
        """
        self.main = main
        self.tree = False
        self.objects_list = pygame.sprite.Group()

    def create_all(self, objects_pos):
        """Créer tout les obstacles"""
        for key in objects_pos.keys():
            #if key == 'fence' and not self.tree:
            #    pass
            #if key == 'tree':
            #    obstacle = Object(self.main, 'fence', objects_pos['fence'])
            #    obstacle.display()
            #    self.objects_list.add(obstacle)

            for pos in objects_pos[key]:
                obstacle = Object(self.main, key, pos)
                obstacle.display()
                self.objects_list.add(obstacle)


class Object(pygame.sprite.Sprite):
    def __init__(self, main, name, pos):
        pygame.sprite.Sprite.__init__(self)

        self.main = main
        self.name = name
        self.pos = pos

        self.image = main.obstacles_images[name]

        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.collision_rect = self.image.get_rect()
        self.collision_rect.x = self.rect.x
        self.collision_rect.y = self.rect.y
        self.collision_rect.inflate_ip(constants.OBSTACLES[name][1][0], constants.OBSTACLES[name][1][1])
        self.collision_rect.center = (self.rect.x + constants.OBSTACLES[name][2][0], self.rect.y + constants.OBSTACLES[name][2][1])

        self.mask = pygame.mask.from_surface(self.image)

    def display(self):
        """Pose l'objet sur le fond"""
        self.main.background.blit(self.image, self.pos)
