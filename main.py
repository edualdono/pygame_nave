import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()
#declaramos el tamanio de la pnatlla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave_Espacial")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.centerx = 30
        self.rect.bottom = HEIGHT // 2 + 50
        self.speed_x = 0
    
    def update(self):
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speed_y = -5
            #print(self.rect.top)
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
            #print(self.rect.bottom)
        self.rect.y += self.speed_y
        
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            
        if self.rect.top < 0:
            self.rect.top = 0

class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            'assets\meteorGrey_med1.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(840, 900)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speedx = random.randrange(-5 , -1)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.x = random.randrange(840, 900)
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.speedx = random.randrange(-5, -1)


background = pygame.image.load("assets/background.png").convert()

all_sprites = pygame.sprite.Group()

player = Player()
meteoro_list = pygame.sprite.Group()

all_sprites.add(player)

for i in range(10):
    meteoro = Meteoro()
    all_sprites.add(meteoro)
    meteoro_list.add(meteoro)

running = True
while running:
    clock.tick(60)
    #buscamso el evento qque cierre la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, meteoro_list, False)
    for hit in hits:
        meteoro = Meteoro()
        all_sprites.add(meteoro)
        meteoro_list.add(meteoro)
    #background
    screen.blit(background, [0, 0])

    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
