import random
import math
import pygame

class Particle:
    def __init__(self, x, y, vel_x, vel_y, lifetime, parent_list):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.lifetime = lifetime
        self.parent_list = parent_list
        self.parent_list.append(self)

    def update(self, gravity_field):

        # Parçacıkların hızını gezegenlerin yerçekimi etkisine göre güncellediğim kısım.
        for planet in gravity_field:
            dx = planet.x - self.x
            dy = planet.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < planet.radius:  # Gezegenin içine girmesin
                self.parent_list.remove(self)
                return

            force = (planet.gravity_constant/3) / (distance ** 3)
            angle = math.atan2(dy, dx)
            self.vel_x += force * math.cos(angle)
            self.vel_y += force * math.sin(angle)


        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.parent_list.remove(self)

    def draw(self, screen):

        if self.lifetime > 0:
            alpha = max(0, int(255 * (self.lifetime / 100)))  # Opaklık ayaryımıs
            color = (alpha, alpha, alpha)  # Gri ton
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 2)
