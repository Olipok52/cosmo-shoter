from pygame import *
from time import time as timer
from random import randint

window = display.set_mode((700,600))
display.set_caption("Space")
background = transform.scale(image.load("galaxy.jpg"), ((700,600)))

clock = time.Clock()
FPS = 60

class GameSprits(sprite.Sprite):
    def __init__(self, sprite, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite), ((size_x,size_y)))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprits):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fier(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

score = 0
lost = 0
amo = 50
reload_time = False

class Enemy(GameSprits):
    def update (self):
        self.rect.y += self.speed
        global lost
        global score
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 700-80)
            lost = lost + 1
            score = score - 5
    
class Bullet(GameSprits):
    def update (self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.rect.y = 490
            self.kill()

asteroids = sprite.Group()
enemys = sprite.Group()
bullets = sprite.Group()
enemys.add(Enemy("ufo.png",100,1,65,65,randint(1,4)))
enemys.add(Enemy('ufo.png',250,1,65,65,randint(1,4)))
enemys.add(Enemy('ufo.png',400,1,65,65,randint(1,4)))
enemys.add(Enemy('ufo.png',550,1,65,65,randint(1,4)))
asteroids.add(Enemy('asteroid.png', 50, 1, 65, 65, randint(2,5)))
asteroids.add(Enemy('asteroid.png', 580, 1, 65, 65, randint(3,5)))

player = Player('rocket.png', 250, 500, 65, 65, 8)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

shot = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 24)

font2 = font.SysFont('Arial', 48)

LOSE = font1.render(
'',1, (255,0,0))

WIN = font1.render(
'',1, (0,255,0))

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False     
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if amo > 0 and reload_time==False:
                    amo -=1
                    player.fier()
                    shot.play()
                if amo == 0 and reload_time==False:
                    perezaradka = timer()
                    reload_time = True
                
    if not finish:
        text_lose = font1.render(
            'Пропущено:' + str(lost), 1 ,(255,255,255)
        )

        text_score = font1.render(
            'счет:' + str(score), 1 ,(255,255,255)
        )

        text_reload = font1.render(
            'Перезарядка', 1 ,(255,255,255) 
        )

        totalamo = font1.render(
            str(amo) + '/50', 1, (255,255,255)
        )

        if lost == 15:
            LOSE = font2.render(
                'Поражение', 1 ,(255,0,0)
            )
            finish = True
        
        if score == 15:
            WIN = font2.render(
                'Победа', 1 ,(0,255,0)
            )
            finish = True
        
        if score <= -50:
            LOSE = font2.render(
                'Поражение', 1 ,(255,0,0)
            )
            finish = True

        sprites_list = sprite.groupcollide(enemys, bullets, True, True)
        for game in sprites_list:
            score +=1
            amo += 1
            enemys.add(Enemy("ufo.png",randint(20,480),1,65,65,randint(1,5)))

        if sprite.spritecollide(player, enemys, True):
            score += 1
            enemys.add(Enemy("ufo.png",randint(20,480),1,65,65,randint(1,5)))
        
        sprites_list2 = sprite.groupcollide(asteroids, bullets, True, True)
        for game in sprites_list2:
            asteroids.add(Enemy('asteroid.png', randint(20,505), 1, 65, 65, randint(3,5)))
        
        if sprite.spritecollide(player, asteroids, True):
            asteroids.add(Enemy("asteroid.png",randint(20,480),1,65,65,randint(1,5)))

        window.blit(background, (0,0))
        window.blit(text_lose,(5,50)) 
        window.blit(text_score,(5,10))
        window.blit(LOSE,(250,250))
        window.blit(WIN,(250,250))
        window.blit(totalamo, (500,500))
        player.update()
        player.reset()
        enemys.draw(window)
        enemys.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        
        if reload_time == True:
                perezaradka_now = timer()
                if (perezaradka_now - perezaradka) < 1.5:
                    window.blit(text_reload, (500,450))
                else:
                    amo = 50
                    reload_time = False        
        clock.tick(FPS)

        display.update()