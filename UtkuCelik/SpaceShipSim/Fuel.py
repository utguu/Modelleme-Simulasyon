import random
import math

class Fuel:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.radius = 15  # Yakıtın boyutu

    @staticmethod
    def spawn_fuels(num_fuels, planets, width, height, fuel_sprite):
        fuels = []
        for _ in range(num_fuels):
            while True:
                x = random.randint(50, width - 50)
                y = random.randint(50, height - 50)

                # Gezegenlerin içinde spawnlanmasın diye
                overlap = False
                for planet in planets:
                    distance = math.sqrt((x - planet.x) ** 2 + (y - planet.y) ** 2)
                    if distance < planet.radius + 50:
                        overlap = True
                        break

                if not overlap:
                    fuels.append(Fuel(x, y, fuel_sprite))
                    break

        return fuels

    def draw(self, screen):

        screen.blit(self.sprite, (self.x - self.radius, self.y - self.radius))
