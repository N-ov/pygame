import pygame

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
FPS = 60
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


def load_image(name):
    return pygame.image.load('textures\\' + name).convert_alpha()


class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("knight stay.png")
        self.walkLeft = [load_image("knight walk left1.png"), load_image("knight walk left2.png")]
        self.walkRight = [load_image("knight walk right1.png"), load_image("knight walk right2.png")]
        self.walkTop = [load_image("knight walk top1.png"), load_image("knight walk top2.png")]
        self.walkBottom = [load_image("knight walk bottom1.png"), load_image("knight walk bottom2.png")]
        self.rect = self.image.get_rect()
        screen.blit(self.image, (0, 0))
        self.animCount = 0
        self.speedx = 0
        self.speedy = 0

    def update(self, *args):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if self.animCount + 1 >= 60:
            self.animCount = 0
        if keystate[pygame.K_a] and not self.rect.left < 0:
            self.speedx = -3
            self.image = self.walkLeft[self.animCount // 30]
            self.animCount += 1
        elif keystate[pygame.K_d] and not self.rect.right > width:
            self.speedx = 3
            self.image = self.walkRight[self.animCount // 30]
            self.animCount += 1
        elif keystate[pygame.K_s] and not self.rect.bottom > height:
            self.speedy = 3
            self.image = self.walkBottom[self.animCount // 30]
            self.animCount += 1
        elif keystate[pygame.K_w] and not self.rect.top < 0:
            self.speedy = -3
            self.image = self.walkTop[self.animCount // 30]
            self.animCount += 1
        else:
            self.animCount = 0
            self.image = load_image("knight stay.png")
        self.rect.x += self.speedx
        self.rect.y += self.speedy


character = Character()
all_sprites.add(character)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    grass = load_image("grass.png")
    pygame.display.set_caption("Heroes 1")
    grass = pygame.transform.scale(grass, (1000, 1000))
    screen.blit(grass, (0, 0))
    character = Character()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        screen.blit(grass, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
