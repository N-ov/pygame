import pygame
import random
import math


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
FPS = 60
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
game_data = {
    'oreId': 0,
    'ores': [],
    'oreClasses': []
}


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
        self.castle = Castle()
        self.wood = 0
        self.gold = 0
        self.cooper = 0
        self.iron = 0
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


class Castle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("Castle 1 lvl.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        screen.blit(self.image, (0, 0))
        self.lvl = 1
        self.rect.x = 750
        self.rect.y = 75

    def update(self, *args):
        if self.lvl == 1:
            pass
        elif self.lvl == 2:
            self.image = load_image("Castle 2 lvl.png")
            self.image = pygame.transform.scale(self.image, (200, 200))
        elif self.lvl == 3:
            self.image = load_image("Castle 3 lvl.png")
            self.image = pygame.transform.scale(self.image, (255, 255))
            self.rect.x = 725
        elif self.lvl == 4:
            self.image = load_image("Castle 4 lvl.png")
            self.image = pygame.transform.scale(self.image, (300, 300))
            self.rect.x = 675

    def quest(self):
        pass


class Ore(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = load_image('iron_ore.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width)
        self.rect.y = random.randint(0, height)
        self.image = pygame.transform.scale(self.image, (70, 70))
        game_data['ores'].append({
            'id': game_data['oreId'],
            'type': 'iron',
            'position': {
                'x': self.rect.x,
                'y': self.rect.y
            }
        })
        self.oreId = game_data['oreId']
        game_data['oreId'] += 1

    def collect(self):
        self.rect.y += width + 100
        self.rect.x += height + 100

        for i in game_data['ores']:
            if i['id'] == self.oreId:
                game_data['ores'].remove(i)


character = Character()
castle = Castle()


def collectOre(pos):
    for ore in game_data['ores']:
        orex, orey = ore['position']['x'], ore['position']['y']
        if math.sqrt((orex - pos.x) ** 2 + (orey - pos.y) ** 2) < 50:
            for oreClass in game_data['oreClasses']:
                if oreClass.oreId == ore['id']:
                    oreClass.collect()


for i in range(10):
    ores = Ore()
    all_sprites.add(ores)
    game_data['oreClasses'].append(ores)

all_sprites.add(character, castle)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    grass = load_image("grass.png")
    pygame.display.set_caption("Heroes 1")
    grass = pygame.transform.scale(grass, (1000, 1000))
    screen.blit(grass, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    collectOre(character.rect)
        all_sprites.update()
        screen.blit(grass, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
