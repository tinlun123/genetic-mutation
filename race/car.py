#!/usr/bin/env python
from collections import namedtuple
import math
import pygame
import obstacle

Vector = namedtuple('Vector', 'x y')


class Car:
    """ Car class """
    # Display window
    window = None

    def __init__(self, x, y, color_chassis):
        self.position = Vector(x, y)
        # 0 = East
        self.direction = 90
        self.speed = 5
        # Radius of the car (because it's a circle)
        self.radius = 20
        # Change in direction, + is right, - is left from the bottom
        self.d_direction = 0
        self.color_chassis = color_chassis
        # Direction arrow
        self.color_direction = color_chassis
        # Direction arrow
        self.arrow_length = self.radius + 5

    def update(self):
        self.direction += self.d_direction
        # Normalize direction to 0 - 360
        if self.direction > 360:
            self.direction - 360
        if self.direction < 0:
            self.direction + 360
        # Calculate position
        new_x = self.position.x + math.cos(math.radians(self.direction)) * self.speed
        new_y = self.position.y - math.sin(math.radians(self.direction)) * self.speed
        self.position = Vector(new_x, new_y)

    def vector_closest_obs(self, obs_list):
        """ Returns the vector to the closest obstacle """
        closest_ob = None
        closest_dist = 99999
        for ob in obs_list:
            dist = obstacle.distance(self.position.x, self.position.y, ob.position.x, ob.position.y)
            if dist < closest_dist:
                closest_ob = ob
                closest_dist = dist
        return Vector(closest_ob.position.x - self.position.x, (closest_ob.position.x - self.position.x))

    def vectorize_direction(self):
        """ Turn direction into a vector """
        # Convert direction to radians for easier computation
        rad_dir = math.radians(self.direction)
        return Vector(math.cos(rad_dir), math.sin(rad_dir))

    def draw(self):
        pygame.draw.circle(self.window,
                           self.color_chassis,
                           (int(self.position.x), int(self.position.y)),
                           self.radius,
                           1)
        pygame.draw.line(self.window,
                         self.color_direction,
                         (int(self.position.x), int(self.position.y)),
                         (int(self.position.x + math.cos(math.radians(self.direction)) * self.arrow_length),
                             int(self.position.y - math.sin(math.radians(self.direction)) * self.arrow_length)))
