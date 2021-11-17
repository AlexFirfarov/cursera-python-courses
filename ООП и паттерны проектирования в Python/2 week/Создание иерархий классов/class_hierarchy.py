#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, coordinates):
        if isinstance(coordinates, tuple) and len(coordinates) == 2:
            self.coordinates = coordinates
        else:
            raise TypeError

    def __getitem__(self, item):
        return self.coordinates[item]

    def __sub__(self, other):
        return Vec2d((self[0] - other[0], self[1] - other[1]))

    def __add__(self, other):
        return Vec2d((self[0] + other[0], self[1] + other[1]))

    def __mul__(self, k):
        return Vec2d((self[0] * k, self[1] * k))

    def __len__(self):
        return math.sqrt(self[0] * self[0] + self[1] * self[1])

    def int_pair(self):
        return self.coordinates


class Polyline:

    def __init__(self, gameDisplay):
        self.points = []
        self.speeds = []
        self.gameDisplay = gameDisplay

    def increase_speeds(self):
        for i in range(0, len(self.speeds)):
            self.speeds[i] = Vec2d(tuple(map(lambda x: x * 1.5, self.speeds[i].coordinates)))

    def decrease_speeds(self):
        for i in range(0, len(self.speeds)):
            self.speeds[i] = Vec2d(tuple(map(lambda x: x / 1.5, self.speeds[i].coordinates)))

    def add_point(self, point):
        if isinstance(point, Vec2d):
            self.points.append(point)
            self.speeds.append(Vec2d((random.random() * 2, random.random() * 2)))
        else:
            raise TypeError

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = Vec2d((-self.speeds[p][0], self.speeds[p][1]))
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = Vec2d((self.speeds[p][0], -self.speeds[p][1]))

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.gameDisplay, color,
                                 (int(points[p_n][0]), int(points[p_n][1])),
                                 (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(self.gameDisplay, color,
                                   (int(p[0]), int(p[1])), width)


class Knot(Polyline):

    def __init__(self, gameDisplay, count):
        super().__init__(gameDisplay)
        self.additional_points = []
        self.count = count

    def delete_last_point(self):
        if len(self.points) * len(self.speeds) != 0:
            self.points.pop()
            self.speeds.pop()
            self.additional_points = self.get_knot()

    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.__get_point(points, alpha, deg - 1) * (1 - alpha)

    def __get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.__get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.__get_points(ptn))
        return res

    def set_points(self):
        super().set_points()
        self.additional_points = self.get_knot()

    def add_point(self, point):
        super().add_point(point)
        self.additional_points = self.get_knot()


class Game:

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")

        self.working = True
        self.show_help = False
        self.pause = True
        self.hue = 0
        self.start_steps = 35
        self.color = pygame.Color(0)
        self.lines = [Knot(self.gameDisplay, 35)]
        self.current_line = 0

    def add_line(self):
        self.lines.append(Knot(self.gameDisplay, self.start_steps))

    def draw_help(self):
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["A", "Add new line"])
        data.append(["C", "Change current line"])
        data.append(["W", "Increase speed of the current line"])
        data.append(["S", "Decrease speed of the current line"])
        data.append(["X", "Delete last point in current line"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.lines[self.current_line].count), "Current points (current line)"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def start(self):
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        for line in self.lines:
                            line.points = []
                            line.speeds = []
                            line.additional_points = []
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_a:
                        self.add_line()
                        self.current_line = len(self.lines) - 1
                    if event.key == pygame.K_c:
                        self.current_line = (self.current_line + 1) % len(self.lines)
                    if event.key == pygame.K_w:
                        self.lines[self.current_line].increase_speeds()
                    if event.key == pygame.K_s:
                        self.lines[self.current_line].decrease_speeds()
                    if event.key == pygame.K_x:
                        self.lines[self.current_line].delete_last_point()
                    if event.key == pygame.K_KP_PLUS:
                        self.lines[self.current_line].count += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.lines[self.current_line].count -= 1 if self.lines[self.current_line].count > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.lines[self.current_line].add_point(Vec2d(event.pos))

            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            for line in self.lines:
                line.draw_points(line.points)
                line.draw_points(line.additional_points, "line", 3, self.color)
            if not self.pause:
                for line in self.lines:
                    line.set_points()
            if self.show_help:
                self.draw_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


if __name__ == '__main__':
    game = Game()
    game.start()
