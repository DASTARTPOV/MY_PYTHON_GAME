import pygame as p
import random as r

WIDTH = 1000#360
HEIGHT = 1000#480
FPS = 60
BLACK = (0, 0, 0) # R    0..255 G 0..255 B 0..255
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

p.init() #инициализация pygame и музыки pygame
p.mixer.init()
background = p.image.load('fon.jpg')
background_rect = background.get_rect()
all_sprites = p.sprite.Group()
bullets = p.sprite.Group()

class Bullet(p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
#        self.image = p.Surface((5, 10)) #размеры пули
#        self.image.fill(WHITE) # цвет пули
        self.image = p.image.load('laserRed03.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Player(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
#        self.image = p.Surface((50, 50))
#       self.image.fill(BLUE)
        self.image = p.image.load('playerShip1_red.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 30
        self.rect.centerx = WIDTH / 2
        self.speedx = 0
        self.speedy = 0
        self.time = p.time.get_ticks()
        self.HP = 100 # в процентах

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = p.key.get_pressed()
        if keystate[p.K_LEFT]:
            self.speedx = -8
        if keystate[p.K_RIGHT]:
            self.speedx = 8
        if keystate[p.K_UP]:
            self.speedy = -5
        if keystate[p.K_DOWN]:
            self.speedy = 5
        if keystate[p.K_SPACE] and p.time.get_ticks() - self.time > 1: #400
            self.time = p.time.get_ticks()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Enemy(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
#        self.image = p.Surface((40, 40))
#       self.image.fill(RED)
        self.image = p.image.load('meteorBrown_big1.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.x = r.randint(0, WIDTH - 40)
        self.speedx = r.randint(-3, 3)
        self.speedy = r.randint(5, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0 - 100 or self.rect.top > HEIGHT + 100 or self.rect.left > WIDTH + 100:
            self.rect.bottom = 0
            self.rect.x = r.randint(0, WIDTH - 40)
            self.speedx = r.randint(-3, 3)
            self.speedy = r.randint(5, 8)

screen = p.display.set_mode((WIDTH, HEIGHT)) # создание окна
p.display.set_caption('My Game')
clock = p.time.Clock() # для FPS
player = Player()
all_sprites.add(player)
mobs = p.sprite.Group()
for i in range(8):
    mob = Enemy()
    all_sprites.add(mob)
    mobs.add(mob)

running = True
while running:
    clock.tick(FPS)
    # Обработка событий
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
    # Обновление
    all_sprites.update()

    hits = p.sprite.spritecollide(player, mobs, True)
    for hit in hits:
        player.HP -= 10
        mob = Enemy()
        all_sprites.add(mob)
        mobs.add(mob)

    if (player.HP <= 0):
        running = False

    hits = p.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        mob = Enemy()
        all_sprites.add(mob)
        mobs.add(mob)

    # Визуализация (рендеринг)
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # Смена кадра
    p.display.update()
p.quit()