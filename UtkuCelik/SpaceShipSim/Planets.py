import pygame
import random
import math
class Planet:
    WIDTH, HEIGHT = 1200, 800
    def __init__(self, x, y, radius,color=None):
        self.x = x
        self.y = y
        self.radius = radius  # Gezegenin boyutu
        self.mass = radius ** 2  # Kütle, yarıçapın karesiyle orantılı. Bunu farklı gezegenler
        #ve farklı çekim alanalrı için yapıyorum. Her gezegenin boyutuna göre çekim alanı artıyor.
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))  # Rastgele renk
        self.gravity_constant = self.mass *70   # Kütle çekimi


        #Deniz tavsiyesi: gezegenlere hareket
        self.vel_x = random.uniform(-0.3, 0.3)
        self.vel_y = random.uniform(-0.3, 0.3)

    def is_colliding(self, other_planet):
        # İki gezegen arasındaki mesafeyi hesaplama kısmı collide edip etmediğini buluyorum.
        distance = math.sqrt((self.x - other_planet.x) ** 2 + (self.y - other_planet.y) ** 2)
        return distance <= (self.radius + other_planet.radius)

    def merge_with(self, other_planet):
        # Kütle merkezine göre yeni pozisyonumuz
        total_mass = self.mass + other_planet.mass
        new_x = (self.x * self.mass + other_planet.x * other_planet.mass) / total_mass
        new_y = (self.y * self.mass + other_planet.y * other_planet.mass) / total_mass

        # Yeni yarıçap hesaplama (toplam alanlardan)
        new_radius = math.sqrt(self.radius ** 2 + other_planet.radius ** 2)

        # Yeni renk, iki gezegenin renklerinin ortalaması (bunun nasıl çalıştığı çok garip)
        new_color = (
            (self.color[0] + other_planet.color[0]) // 2,
            (self.color[1] + other_planet.color[1]) // 2,
            (self.color[2] + other_planet.color[2]) // 2,
        )

        # Yeni gezegen oluşturuyorum
        return Planet(new_x, new_y, new_radius, new_color)

    def update_position(self):
        # Gezegenin pozisyonunu güncelle
        self.x += self.vel_x
        self.y += self.vel_y

        # Ekranın sınırlarına çarptığında yön değiştir
        if self.x - self.radius < 0 or self.x + self.radius > self.WIDTH:
            self.vel_x = -self.vel_x
        if self.y - self.radius < 0 or self.y + self.radius > self.HEIGHT:
            self.vel_y = -self.vel_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


def generate_planets(num_planets, width, height, spaceship_x, spaceship_y):
    planets = []
    while len(planets) < num_planets:
        x = random.randint(200, width - 200)
        y = random.randint(100, height - 100)
        radius = random.randint(30, 60)  # Gezegen boyutu

        # Gezegen, geminin başlangıç pozisyonuna çok yakınsa gezegeni yeniden oluşturuyorum.
        if math.hypot(x - spaceship_x, y - spaceship_y) < 200:
            continue

        # Gezegenlerin birbirine çok yakın olmaması gerekiyor.
        overlap = False
        for planet in planets:
            distance = math.hypot(x - planet.x, y - planet.y)
            if distance < (radius + planet.radius + 50):  # Minimum mesafe ayarı çekiyorum.
                overlap = True
                break

        if not overlap:
            planets.append(Planet(x, y, radius))

    return planets
