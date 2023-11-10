from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, picture, x, y, w, h):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, picture, x, y, w, h, x_speed, y_speed):
       GameSprite.__init__(self, picture, x, y, w, h)
       self.x_speed = x_speed
       self.y_speed = y_speed
    def update(self):
        if player.rect.x <= winw - 80 and player.x_speed > 0 or player.rect.x >=0 and player.x_speed <= 0:
            self.rect.x += self.x_speed
        platforms = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms:
                self.rect.left = max(self.rect.left, p.rect.right)
        if player.rect.y <= winw - 80 and player.y_speed > 0 or player.rect.y >=0 and player.y_speed <= 0:
            self.rect.y += self.y_speed
        platforms = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('двойка.png', self.rect.right, self.rect.centery, 15,20,15)
        bullets.add(bullet)


class Enemy(GameSprite):
    sait = 'left'
    def __init__(self, picture,  x, y, w, h, speed):
       GameSprite.__init__(self, picture, x, y, w, h)
       self.speed = speed
    def update(self):
        if self.rect.x <= 420:
            self.sait = 'right'
        elif self.rect.x >= winw - 85:
            self.sait = 'left'
        if self.sait == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet (sprite.Sprite):
    def __init__(self, picture, x, y, w, h, speed):
        GameSprite.__init__(self, picture, x, y, w, h)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > winw + 10:
            self.kill()








player = Player('хороший_герой.png', 5, 400, 80, 80, 0, 0)

wall = GameSprite('стена.png', 700/2-700/3, 500/2, 300, 50)
wall1 = GameSprite('стена.png', 370, 100, 50, 400)
chemistrychka = Enemy('химичка_отстой.png', 620, 180, 105, 100, 5)
dimpleim = GameSprite('диплом.png', 620, 400, 50, 50)
barriers = sprite.Group()
bullets = sprite.Group()
fuckers = sprite.Group()
fuckers.add(chemistrychka)
barriers.add(wall)
barriers.add(wall1)
winw = 700
winh = 500
window = display.set_mode((winw, winh))
display.set_caption('гиа 2014!')
backgraund = transform.scale(image.load('огэ.png'), (700, 500))
run = True
finish = False 
while run:
    time.delay(50)
    
    for e in event.get():
        if e.type == QUIT:
           run = False
        if e.type == KEYDOWN:
            if e.key == K_a:
                player.x_speed = -5
            elif e.key == K_d:
                player.x_speed = 5
            elif e.key == K_w:
                player.y_speed = -5
            elif e.key == K_s:
                player.y_speed = 5
            elif e.key == K_SPACE:
                player.fire()




            
        if e.type == KEYUP:
            if e.key == K_a:
                player.x_speed = 0
            elif e.key == K_d:
                player.x_speed = 0
            elif e.key == K_w:
                player.y_speed = 0
            elif e.key == K_s:
                player.y_speed = 0  
    if not finish:
        window.blit(backgraund, (0, 0))

        dimpleim.reset()
        fuckers.draw(window)
        fuckers.update()
        bullets.draw(window)
        bullets.update()
        barriers.draw(window)
        player.reset()
        player.update()
        sprite.groupcollide(fuckers, bullets, True, True)
        sprite.groupcollide(bullets, barriers, True, False)
        if sprite.spritecollide(player, fuckers, False) :
            finish = True
            window.fill((255,255,255))
            image = image.load('проигрыш.png')
            window.blit(transform.scale(image, (winw, winh)),  (0, 0))
        if sprite.collide_rect(player, dimpleim):
            finish = True
            window.fill((255,255,255))
            image = image.load('победа.jpg')
            window.blit(transform.scale(image, (winw, winh)),  (0, 0))
    display.update()
