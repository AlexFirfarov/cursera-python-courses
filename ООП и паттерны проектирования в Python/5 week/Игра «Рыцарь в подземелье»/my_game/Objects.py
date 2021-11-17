from abc import ABC, abstractmethod
import pygame
import random

import Service


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def draw(self, display):
        display.blit(self.sprite, (display.game_engine.sprite_size * display.game_engine.map_left_top[0],
                                   display.game_engine.sprite_size * display.game_engine.map_left_top[1]))


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.exp = xp

    def interact(self, engine, hero):

        k_endurance = hero.stats["endurance"] / (random.randint(engine.level, engine.level + 1) * self.stats["endurance"])
        k_intelligence = hero.stats["intelligence"] / (random.randint(engine.level, engine.level + 1) * self.stats["intelligence"])
        k_luck = hero.stats["luck"] / (random.randint(engine.level, engine.level + 1) * self.stats["luck"])

        hero_power = k_endurance * k_intelligence * k_luck * hero.stats["strength"]

        if hero_power > self.stats["strength"]:
            hero.exp += int(1.2 * self.exp)
            engine.score += 10 * hero.hp
        elif hero_power == self.stats["strength"]:
            hero.exp += self.exp
        else:
            hero.exp += int(0.2 * self.exp)
            hero.hp -= int(0.5 * (self.stats["strength"] - hero_power))
            if engine.hero.hp > 0:
                engine.score += 2 * hero.hp
            else:
                hero.level_up()
                engine.level = 5
                Service.reload_game(engine, hero)
                return

        hero.level_up()
        if hero.hp > hero.max_hp:
            hero.hp = hero.max_hp


class Berserk(Effect):

    def apply_effect(self):
        self.stats["strength"] += 7
        self.stats["endurance"] += 7
        self.stats["luck"] += 7
        self.stats["intelligence"] -= 3


class Blessing(Effect):

    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["luck"] += 2
        self.stats["intelligence"] += 2


class Weakness(Effect):

    def apply_effect(self):
        self.stats["strength"] -= 4
        self.stats["endurance"] -= 4


class Wisdom(Effect):

    def apply_effect(self):
        self.stats["intelligence"] += 20
        self.stats["strength"] -= 8
