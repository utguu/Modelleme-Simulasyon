import pygame
import sys
import random
from SpaceShip import SpaceShip
from Planets import generate_planets
from Hud import HUD
from Fuel import Fuel
from Particles import Particle
# Ekran Ayarları
WIDTH, HEIGHT = 1200, 800
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uzay Gemisi Simülasyonu")
clock = pygame.time.Clock() #Bu fps kontrolü için
font = pygame.font.SysFont("Arial", 24)

# Sprite'lar
idle_sprite = pygame.image.load("ship_idle.png")
thrust_sprite = pygame.image.load("ship_thrust.png")
arrow_sprite = pygame.image.load("arrow.png")

particles = []


def main():
    spaceship = SpaceShip(50, HEIGHT // 2, idle_sprite, thrust_sprite) #gemi sınıfından çektim nesne oluşturdum.
    planets = generate_planets(7, WIDTH, HEIGHT, spaceship.x, spaceship.y)
    hud = HUD(font)

    # Yakıt
    fuel_sprite = pygame.image.load("fuel.png")  # Yakıt görseli
    fuels = Fuel.spawn_fuels(5, planets, WIDTH, HEIGHT, fuel_sprite)

    score = 0

    while True:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Kontroller
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and spaceship.fuel > 0:  # Yakıt varsa thrust uygulamam lazım
            spaceship.thrust = min(spaceship.thrust + 2, spaceship.max_thrust)
        else:
            spaceship.thrust = max(spaceship.thrust - 1, 0)

        if keys[pygame.K_LEFT]:
            spaceship.rotate("left")
        if keys[pygame.K_RIGHT]:
            spaceship.rotate("right")
        """
        if keys[pygame.K_DOWN]:
            spaceship.apply_brake()
        """

        collision = spaceship.apply_gravity(planets)
        if collision:
            print("Gezegen tarafından yutuldun! Oyun bitti.")
            break

        spaceship.apply_thrust()
        spaceship.update_position(dt)
        # Yakıt toplama
        spaceship.collect_fuel(fuels)

        for _ in range(1):  # Her döngüde kaç parçacık oluşsun?
            Particle(
                random.randint(0, WIDTH),  # Rastgele x pozisyonu
                random.randint(0, HEIGHT),  # Rastgele y pozisyonu
                random.uniform(-0.00000000001, 0.00000000001),  # Rastgele x hızı
                random.uniform(-0.00000000001, 0.00000000001),  # Rastgele y hızı
                random.randint(30, 60),  # Rastgele ömür
                particles  # Parçacıkları listeye ekle
            )




        if spaceship.x < 0 or spaceship.y < 0 or spaceship.y > HEIGHT:
            print("Ekranın sınırlarına çarptın! Oyun bitti.")
            break

        # Yeni bölüme geçiş ve skoru arttırma kısmı
        if spaceship.x > WIDTH:
            spaceship.x = 50
            spaceship.y = HEIGHT // 2
            planets = generate_planets(7, WIDTH, HEIGHT, spaceship.x, spaceship.y)
            fuels = Fuel.spawn_fuels(5, planets, WIDTH, HEIGHT, fuel_sprite)  # Yakıtları yeniden oluşturmam lazım
            score += 100

        # Çizimleri burada yapıyorum
        screen.fill((0, 0, 0))  # Ekranı temizle
        # Parçacıkları güncellediğim kısım
        for particle in particles[:]:
            particle.update(planets)
            particle.draw(screen)

        for planet in planets:
            planet.update_position()
            planet.draw(screen)

        # Gezegen çarpışma kontrolü
        for i in range(len(planets) - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                if planets[i].is_colliding(planets[j]):
                    # Çarpışma olursa gezegenleri birleştirme kısmı.
                    new_planet = planets[i].merge_with(planets[j])
                    planets.pop(i)  # Eski gezegeni çıkarıyorum
                    planets.pop(j)  # Diğer gezegeni de çıkarıyorum
                    planets.append(new_planet)  # Yenisini yaratıyoruz
                    break

        for fuel in fuels:
            fuel.draw(screen)

        spaceship.draw(screen)
        hud.draw(screen, spaceship)
        screen.blit(arrow_sprite, (WIDTH - 100, HEIGHT // 2 - 50))

        # Skor gösterimini hudda değil burada yapıyorum çünkü burada hesapladım.
        score_text = font.render(f"Skor: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 150))

        pygame.display.flip()

if __name__ == "__main__":
    main()
