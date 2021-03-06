#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame
import zompixel.constants as constants
from zompixel.character import Humain, Zombie
from zompixel.utils.log_config import LoggerManager

LOGGER = LoggerManager.getLogger("root")


class PNJ(object):
    def __init__(self, main, start_enemy_list, level):
        self.main = main
        self.level = level
        self.pnj_num = 0  # compteur pour différencier les pnjs
        self.init_pnj(start_enemy_list)

    def init_pnj(self, enemy_data):
        """Initialise les Personnages Non Joueur"""
        LOGGER.info("     - PNJ Init in Progress")
        for pos in enemy_data.keys():
            Humain(self.main, enemy_data[pos], pos, self.pnj_num)
            self.pnj_num += 1
            LOGGER.info("."),

    def add_zombie(self, main, name, pos, num):
        """Instancie un zombie"""
        LOGGER.info("[*] " + name + " Going Zombie")
        Zombie(main, name, pos, num)
        LOGGER.info("[*] New Zombie")

    def add_enemy(self, pos):
        """Instancie un enemi"""
        LOGGER.info("[*] Add citizen" + str(self.pnj_num))
        Humain(self.main, "citizen", pos, self.pnj_num)
        self.pnj_num += 1

    def remove_all_zombie(self):
        """Supprime tout les zombies"""
        LOGGER.info("[*] Remove Remaining Zombies")
        for zombie in self.main.zombie_sprites:
            self.main.zombie_sprites.remove(zombie)
            self.main.pnj_sprites.remove(zombie)
            self.main.all_sprites.remove(zombie)

        LOGGER.info("     - Ok")

    def update(self):
        """Met les pnj à jour"""
        # Supprime les pnjs si ils sont 'mort'
        for pnj in self.main.pnj_sprites:
            if not pnj.is_alive:
                self.main.pnj_sprites.remove(pnj)
                self.main.all_sprites.remove(pnj)

                if pnj.is_human:
                    LOGGER.info("[*] Remove Human")
                    self.main.enemy_sprites.remove(pnj)

                else:
                    LOGGER.info("[*] Remove Human")
                    self.main.zombie_sprites.remove(pnj)


class Obstacles(object):
    def __init__(self, main):
        """Gère les différent obstacles"""
        self.main = main
        self.tree = False
        self.objects_list = pygame.sprite.Group()

    def create_all(self, objects_pos):
        """Instancie tout les obstacles"""
        for key in objects_pos.keys():
            for pos in objects_pos[key]:
                obstacle = Object(self.main, key, pos)
                self.objects_list.add(obstacle)

        LOGGER.info("[*] Create Objects Ok")

    def reset(self):
        """Supprime tout les objets instanciés"""
        for object in self.objects_list:
            self.main.all_sprites.remove(object)
            self.objects_list.remove(object)


class Object(pygame.sprite.Sprite):
    def __init__(self, main, name, pos):
        self._layer = 0
        pygame.sprite.Sprite.__init__(self, main.all_sprites)

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
        self.collision_rect.inflate_ip(
            constants.OBSTACLES[name][1][0], constants.OBSTACLES[name][1][1]
        )
        self.collision_rect.center = (
            self.rect.x + constants.OBSTACLES[name][2][0],
            self.rect.y + constants.OBSTACLES[name][2][1],
        )

        self.mask = pygame.mask.from_surface(self.image)
