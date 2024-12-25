import pygame

class HUD:
    def __init__(self, font):
        self.font = font

    def draw(self, screen, spaceship):
        # Hız ve ivme hesaplama. Bu hızı ve ivmeyi ekrana yansıtabilmek için gerekiyor.
        # Geminin toplam hızını (magnitude) hesaplamak için Pisagor Teoremi kullanılıyor.
        # x ve y eksenlerindeki hız bileşenlerinin kareleri toplanır ve karekökü alınıyor.
        # Formül: Hız = sqrt(vel_x^2 + vel_y^2)
        # Geminin o anki ivmesi (hızlanma miktarı) gaz gücüne (thrust) ve kütleye (mass) bağlı.
        # Formül: İvme = Thrust / Mass
        # Daha fazla thrust (gaz) daha fazla ivmeye, daha fazla kütle daha az ivmeye neden olur.

        speed = (spaceship.vel_x ** 2 + spaceship.vel_y ** 2) ** 0.5
        acceleration = spaceship.thrust / spaceship.mass

        # HUD
        hud_texts = [
            f"Hız: {speed:.1f} m/s",
            f"Ivme: {acceleration:.2f} m/s²",
            f"Gaz: {spaceship.thrust:.1f}",
            f"X: {spaceship.x:.1f}, Y: {spaceship.y:.1f}",
            f"Fren Aktif: {'Evet' if spaceship.thrust == 0 else 'Hayır'}"
        ]

        for i, text in enumerate(hud_texts):
            hud_surface = self.font.render(text, True, (255, 255, 255))
            screen.blit(hud_surface, (10, 10 + i * 30))
