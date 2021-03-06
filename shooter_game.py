from pygame import * 
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'

font.init()
font2 = font.Font(None, 36)

score = 0

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

run = True
finish = False
lose = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lose += 1 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

img_ast = 'asteroid.png'
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroid(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1,5))
    asteroids.add(asteroid)

ship = Player(img_hero, 5, win_height -100, 80, 100, 10)

img_enemy = 'ufo.png'
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

img_bullet = 'bullet.png'
bullets = sprite.Group()

font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lost = font1.render('YOU LOSE!', True, (255,0,0))
max_lost = 4

fire_sound = mixer.Sound('fire.ogg')

from time import time as timer
rel_time = False
num_fire = 0
goal = 30
life = 3

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire() 
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
     
    if not finish:
        window.blit(background, (0,0))

        text = font2.render('????????:' + str(score), 1,(255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('??????????????????:' + str(lose), 1,(255, 255, 255))
        window.blit(text_lose, (10,50))

        monsters.update()
        monsters.draw(window)

        ship.update()
        ship.reset()

        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('???????? ??????????????????????...', 1, (255,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1
        if life == 0 or lose >= max_lost:
            finish = True
            window.blit(lost, (200, 200))

        if score>= goal:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life_color == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650,10))

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for m in asteroids:
            m.kill()

        time.delay(300)
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Asteroid(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1,5))
            asteroids.add(asteroid)
    time.delay(50)
    
    

