from time import *
import pygame as pg
from random import *
pg.init()

GREEN = (0, 255, 0)

pg.mixer.init()
pg.mixer.music.load('space.ogg')
pg.mixer.music.play()
fire = pg.mixer.Sound('fire.ogg')
#boom_sound = pg.mixer.Sound('boom1.ogg')

class BaseSprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y, w, h, speed_x=0, speed_y=0, energy=0, health=100, points=0):
        super().__init__()
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.image = pg.transform.scale(pg.image.load(filename), (w, h))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.energy = energy
        self.health = health
        self.points = points

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

class Star(BaseSprite):
    def update(self):
        super().update()
        if self.rect.y > win_size[y]:
            stars.remove(self)

class UFO(BaseSprite):
    def update(self):
            global ufo_missed
            super().update()
            if self.rect.y > win_size[y]:
                self.kill()
                ufo_missed += 1

class UFO2(BaseSprite):
    def update(self):
            global ufo_missed
            super().update()
            if self.rect.y > win_size[y]:
                self.kill()
                ufo_missed += 1

class Hero(BaseSprite):
    enegry = 0
    health = 100
    points = 0

    def update(self):
        self.energy += 1
        self.draw_health()
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed_x
            
        if keys[pg.K_RIGHT] and self.rect.x <= win_size[0] - self.rect.width:            
            self.rect.x += self.speed_x 
            
        if keys[pg.K_UP] and self.rect.y >= 5:
            self.rect.y -= self.speed_y 
              
        if keys[pg.K_DOWN] and self.rect.y <= win_size[1] - self.rect.height:            
            self.rect.y += self.speed_y
        
        if keys[pg.K_SPACE]:                       
                self.fire()

    def draw_health(self):
        rect1 = pg.Rect(self.rect.x, 
                        self.rect.bottom,
                        self.rect.width / 100 * self.health, 
                        8)
        rect2 = pg.Rect(self.rect.x, 
                        self.rect.bottom,
                        self.rect.width, 
                        9)
        g = int(255/100*self.health)
        if g<0:
            g = 0
        r = int(255 - g)
        b = 50
        pg.draw.rect(mw,(r, g, b), rect1)   
        pg.draw.rect(mw,(200, 200, 30), rect2, 4)   

    def draw(self):
        super().draw() 
        self.draw_health()


    def fire(self):
        if self.energy >= 30:
            self.energy = 0
        w = 16
        h = 40
        bullet = Bullet('bullet.png', self.rect.x + self.rect.width/2 - w/2,
                        self.rect.y - h,
                        w, h, 
                        speed_x = 0, speed_y = -5)
        bullets.add(bullet)
        all_sprite.add(bullet)

class Bullet(BaseSprite):
    pass

def set_text(text, x, y, color=(255,255,200)):
    mw.blit(
        font1.render(text, True, color),(x,y)
    )
    
def spawn_star():
    size = randint(15, 40)
    star = Star('star.png', randint(0, win_size[x]), -10, size, size, 0, randint(2, 9))
    stars.add(star)
    all_sprite.add(star)

def spawn_ufo():
    ufo = UFO('ufo.png', randint(0, win_size[x]-90), -100, 90, 90, 0, randint(1, 4), 0, health=2)
    ufos.add(ufo)
    all_sprite.add(ufo)

def spawn_ufo2():
    ufo2 = UFO2('ufo2.png', randint(0, win_size[x]-90), -100, 50, 30, 0, randint(3, 6))
    ufos2.add(ufo2)
    all_sprite.add(ufo2)
        
class Boom(pg.sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms) -> None:
        super().__init__() 
        #global booms, boom_sprites              
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
        self.add(all_sprite)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        if self.frame_num > len(self.frames)-1:
            self.frame_num = 0
        
    def update(self):
        self.next_frame()
        if self.frame_num == len(self.frames)-1:
            self.kill()

class Meteor(pg.sprite.Sprite):
    def __init__(self, speed_x, speed_y, center, meteor_sprites, meteors) -> None:
        super().__init__() 
        #global meteor, meteor_sprites              
        self.frames = meteor_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = meteor_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.add(meteors)
        self.add(all_sprite)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        if self.frame_num > len(self.frames)-1:
            self.frame_num = 0
        
    def update(self):
        self.next_frame()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

def spawn_meteor():
    s_x = randint(-5, 5)
    s_y = randint(5, 10)
    x = randint(-80, 680)
    Meteor(s_x, s_y, (x, -80), choice(meteor_sprites), meteors)

def sprites_load(folder, file_name, size, colorkey=(0,0,0)):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            spr = pg.image.load(f'{folder}\\{file_name}{num}.png')
            spr = pg.transform.scale(spr,size)
            if colorkey: spr.set_colorkey(colorkey)
            sprites.append(spr)
            num += 1
        except:
            load = False
    return sprites

pg.font.init()
font1 = pg.font.Font(None, 36)

win_size = (800, 600)
x, y = 0, 1

mw = pg.display.set_mode(win_size)
# mw = pg.display.set_mode(win_size, pg.FULLSCREEN)
pg.display.set_caption("Shooter")
clock = pg.time.Clock()

fon = pg.transform.scale(
                            pg.image.load("cosmos.jpg"), win_size
                            )
fon_go = pg.transform.scale(
                            pg.image.load("gameover.png"), win_size
                            )
#fon_win = pg.transform.scale(pg.image.load("win.png"), win_size)

hero = Hero("ship.png", 360, 490, 80, 80, 5, 5)


font1 = pg.font.Font(None, 40)

boom_sprites = sprites_load('boom4', 'boom', (80,80))
meteor_sprites = [
    sprites_load('meteor1', 'meteor', (20,20)),
    sprites_load('meteor1', 'meteor', (30,30)),
    sprites_load('meteor1', 'meteor', (40,40)),
    sprites_load('meteor1', 'meteor', (50,50)),
]

#print(len(boom_sprites))

heros = pg.sprite.Group()
booms = pg.sprite.Group()
meteors = pg.sprite.Group()
stars = pg.sprite.Group()
ufos = pg.sprite.Group()
ufos2 = pg.sprite.Group()
bullets = pg.sprite.Group()
all_sprite = pg.sprite.Group()

heros.add(hero)
all_sprite.add(hero)

play = True
win = False
game = True
ticks = 1
ufo_missed = 0

while play:
    for e in pg.event.get():
        if e.type == pg.QUIT or \
                    (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                play  = False

    if game:

        if ticks % 20 == 0: spawn_star()
        if ticks % 120 == 0: spawn_ufo()
        if ticks % 350 == 0: spawn_ufo2()
        if ticks % 120 == 0: spawn_meteor()


        mw.blit(fon, (0, 0))

        all_sprite.update()
        all_sprite.draw(mw)

        if pg.sprite.spritecollide(hero, ufos, False):
            Hero.health -= 1
        if pg.sprite.spritecollide(hero, meteors, False):
            Hero.health -= 1

        collides = pg.sprite.groupcollide(bullets, ufos, True, True)
        for bullet, ufo in collides.items():
            Boom(ufo[0].rect.center, boom_sprites, booms)
            hero.points +=1
            #boom_sound.play()

        collidis = pg.sprite.groupcollide(bullets, ufos2, True, True)
        for bullet, ufo2 in collidis.items():
            if ufo2[0].health == 0:
                Boom(ufo2[0].rect.center, boom_sprites, booms)
                hero.points +=1

        set_text(f"Пропущено: {ufo_missed}", 600, 20)

    else:
        mw.blit(fon_go, (0, 0))


    pg.display.update()
    clock.tick(60)
    ticks += 1
