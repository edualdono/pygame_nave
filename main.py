import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()
#declaramos el tamanio de la pnatlla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE QUEST")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    #declaramos la fuente a utilizar
    font = pygame.font.SysFont("serif" , size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x , y)
    surface.blit(text_surface, text_rect)

def draw_lives(lives):
    image = pygame.image.load('assets/player.png').convert()
    image.set_colorkey(BLACK)
    scale_factor = 0.5
    new_width = int(image.get_width() * scale_factor)
    new_height = int(image.get_height() * scale_factor)
    factor_size = 30
    for i in range(lives):
        resized_image = pygame.transform.scale(image, (new_width, new_height))
        resized_rect = resized_image.get_rect()
        resized_rect.midtop = (WIDTH - factor_size - (i*50) , 10)
        screen.blit(resized_image, resized_rect)

def draw_planet():
    image = pygame.image.load('assets/planet.png').convert()
    image.set_colorkey(BLACK)
    scale_factor = 1.5
    new_width = int(image.get_width() * scale_factor)
    new_height = int(image.get_height() * scale_factor)
    resized_image = pygame.transform.scale(image, (new_width, new_height))
    resized_rect = resized_image.get_rect()
    resized_rect.midtop = (WIDTH + 150, 0)
    screen.blit(resized_image, resized_rect)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.centerx = 30
        self.rect.bottom = HEIGHT // 2 + 50
        self.speed_y = 0
    
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
    def __init__(self, vel_max, vel_min):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(840, 900)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speedx = random.randrange(vel_max, vel_min)

    def update(self, flag):
        self.rect.x += self.speedx
        if self.rect.left < 0 and flag == False:
            self.image = random.choice(meteor_images)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(840, 900)
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.speedx = random.randrange(vel_max, vel_min)

class Planet(pygame.sprite.Sprite):
    def __init__(self,):
        super().__init__()
        self.image = pygame.image.load('assets/planet.png').convert()
        self.image.set_colorkey(BLACK)
        scale_factor = 1.5
        new_width = int(self.image.get_width() * scale_factor)
        new_height = int(self.image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 0
        self.speedx = -2
    
    def update(self):
        if self.rect.x < 950:
             self.rect.x = 950
        else:
            self.rect.x += self.speedx



class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50  # velocidad de la animcion

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()  # matamos el objeto unavez que se termina de reproducir11111111
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center
                                

def show_go_screen():
	screen.blit(background, [0, 0])
	draw_text(screen, "THE QUEST", 65, WIDTH // 2, HEIGHT // 4)
	draw_text(screen, "Instruciones van aquí", 27, WIDTH // 2, HEIGHT // 2)
	draw_text(screen, "Presiona cualquier Tecla", 20, WIDTH // 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

def show_lup_screen(level):
    screen.fill(BLACK)
    draw_text(screen, "LEVEL " + str(level), 27, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    counter = 0
    while waiting:
        clock.tick(60)
        counter +=1
        if counter == 120:
            waiting = False

        
#cargar imagenes de los meteoros
meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
               "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
               "assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())
        
#cargar animacion de explosion
explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)


#cargar background        
background = pygame.image.load("assets/background.png").convert()

#cargar sonidos
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.1)


# loop infinito con -1
pygame.mixer.music.play(loops=-1)

contador = 0
#game_over = True
running = True
lives = 0
vel_max = -5
vel_min = -1
num_meteoros = 8
level_up = False

while running:
    if lives == 0:
        show_go_screen()

        #game_over = False
        all_sprites = pygame.sprite.Group()
        meteoro_list = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        score = 0
        lives = 3

        for i in range(8):
            meteoro = Meteoro(vel_max,vel_min)
            #all_sprites.add(meteoro)
            meteoro_list.add(meteoro)

    #print(score % 6)

    #aumento de nivel
    if score % 60 == 0 and contador == 0 and score != 0:
        #----animacion-fin-nivel---------
        level_up = True
        planeta = Planet()
        all_sprites.add(planeta)

        while level_up:
            clock.tick(60)
            contador += 1
            all_sprites.update()
            meteoro_list.update(level_up)
            screen.blit(background, [0, 0])
            all_sprites.draw(screen)
            meteoro_list.draw(screen)
            pygame.display.flip()
            if contador > 600:
                 level_up = False
                 contador = 0

        num_meteoros += 1
        vel_max -= 1
        vel_min -= 0

        all_sprites = pygame.sprite.Group()
        meteoro_list = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        for i in range(num_meteoros):
            meteoro = Meteoro(vel_max, vel_min)
            #all_sprites.add(meteoro)
            meteoro_list.add(meteoro)

        show_lup_screen(score // 60 + 1)
        #print('Aumenta nivel')

    clock.tick(60)

    contador += 1

    if contador == 60:
        score +=1
        contador = 0
    #buscamso el evento qque cierre la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    meteoro_list.update(level_up)

    hits = pygame.sprite.spritecollide(player, meteoro_list, True)
    if hits:
        explosion_sound.play()
        explosion = Explosion(player.rect.center)
        all_sprites.add(explosion)
        lives -= 1 
        meteoro = Meteoro(vel_max, vel_min)
        #all_sprites.add(meteoro)
        meteoro_list.add(meteoro)
        #print(len(meteoro_list))
        #game_over = True
    #background
    screen.blit(background, [0, 0])

    all_sprites.draw(screen)
    meteoro_list.draw(screen)

    #marcador
    draw_text(screen, "PUNTUACION", 20, WIDTH // 2, 10)
    draw_text(screen, str(score), 30, WIDTH // 2, 30)
    draw_lives(lives)
    #draw_planet()

    pygame.display.flip()

pygame.quit()
