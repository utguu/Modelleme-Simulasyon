import pygame
import math

class SpaceShip:
    def __init__(self, x, y, idle_sprite, thrust_sprite):
        # Constructor metodum burada geminin bileşenlerini tanımlıyorum.
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.angle = 0
        self.thrust = 0
        self.max_thrust = 300
        self.mass = 10
        self.angular_velocity = 0 #Açısal hızım (radyan/saniye şeklinde)
        self.width=50
        self.height=50
        self.sprite_idle = idle_sprite
        self.sprite_thrust = thrust_sprite

        # Yakıt Sistemi
        self.fuel = 5000
        self.fuel_burn_rate = 2

        self.inertia = self.mass*(self.width/2)**2 #Atalet momenti bu açısal hızı dinamik hale getirmek için
        #tork ile birleştiricem

    def apply_thrust(self):
        # Eğer yakıt varsa hareket et
        if self.thrust > 0 and self.fuel>0:
            # Yöne göre hız eklediğim kısım
            force_x = self.thrust * math.cos(math.radians(self.angle))
            force_y = self.thrust * math.sin(math.radians(self.angle))
            # Kütleye göre kuvveti hıza dönüştürüyorum.
            self.vel_x += force_x / self.mass / 60
            self.vel_y += force_y / self.mass / 60

            # Yakıtı azaltma
            self.fuel -= self.fuel_burn_rate
        if self.fuel<0:
            self.fuel=0

    """
    def apply_brake(self):
        # Frenleme: geriye doğru thrust uyguluyorum ve hızı da çarpanla azaltıyorum. Araba gibi hemen
        # fren yapmak istemiyorum. Bu olunca gezegenlerin çekim alanına bile karşoı koyabiliyoruz.
        brake_force = 3
        #İleri versiyonun geri hali.
        force_x = brake_force * math.cos(math.radians(self.angle + 180))
        force_y = brake_force * math.sin(math.radians(self.angle + 180))
        self.vel_x += force_x / self.mass / 60
        self.vel_y += force_y / self.mass / 60

        # Hızın kademeli azalması için bunu düşük bir değer ilşe çarıpıyorum.
        self.vel_x *= 0.995  # Daha yavaş yavaşlama 
        self.vel_y *= 0.995
    """
    def apply_gravity(self, planets):
        for planet in planets:
            dx = planet.x - self.x
            dy = planet.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # Çekim etkisinı ayarlıyorum burada.
            if 50 < distance < 1000:  # Gezegen çekim alanı en makul olanı bu gibi.
                force = planet.gravity_constant / (distance ** 3)
                angle = math.atan2(dy, dx)
                self.vel_x += (force * math.cos(angle)) / 60
                self.vel_y += (force * math.sin(angle)) / 60

            if distance < planet.radius:
                return True  # Gezegen ile çarpışma durumu
        return False

    def rotate(self, direction):
        torque=50
        rotational_drag = 0.2

        #Acisal ivme hesaplamasi
        angular_acceleration=torque/self.inertia
        #Acisal hiz ve ivme kullanarak yon
        if direction == "left":
            self.angular_velocity -= angular_acceleration
        elif direction == "right":
            self.angular_velocity += angular_acceleration

        # Donusu yavaslatmak icin (surtunme)
        self.angular_velocity *= (1 - rotational_drag)

        # Aciyi guncelleme
        self.angle += math.degrees(self.angular_velocity)
        self.angle %= 360  # Aciyi 0-360 arasında tutmak icin



    def update_position(self, dt):
        # Geminin pozisyonunu güncelleme
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

    def draw(self, screen):
        # Yakıt göstergesi
        fuel_text = pygame.font.SysFont("Arial", 24).render(f"Yakıt: {self.fuel}", True, (255, 255, 255))
        screen.blit(fuel_text, (10, 50))

        # Thrust sprite'ını yalnızca thrust > 0 ve yakıt > 0 ise göster
        if self.thrust > 0 and self.fuel > 0:
            rotated_sprite = pygame.transform.rotate(self.sprite_thrust, -self.angle)
        else:
            rotated_sprite = pygame.transform.rotate(self.sprite_idle, -self.angle)

        rect = rotated_sprite.get_rect(center=(self.x, self.y))
        screen.blit(rotated_sprite, rect)

    def collect_fuel(self, fuels):

        for fuel in fuels[:]:
            distance = math.sqrt((self.x - fuel.x) ** 2 + (self.y - fuel.y) ** 2)
            if distance < fuel.radius + 20:
                self.fuel += 1000
                if self.fuel > 5000:
                    self.fuel = 5000
                fuels.remove(fuel)