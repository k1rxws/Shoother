from pygame import *
from random import randint

init()

mixer.music.load("song.ogg")
mixer.music.play(-1)

win_width = 700
win_height = 500

img_background = "black.png"
img_hero = "rocket.png"
img_enemy1 = "enemyBlack.png"
img_enemy2 = "enemyGreen.png"
img_enemy3 = "enemyRed.png"
img_bullet = "bullet.png"
start_img = "start_btn.png"
exit_img = "exit_btn.png"
restart_img = "restart_btn.png"

fire = mixer.Sound('sfx_laser1.ogg')
shot = mixer.Sound('sfx_twoTone.ogg')
enemy_down = mixer.Sound('sfx_shieldDown.ogg')

lost = 0
score = 0

game = True
main_menu = True

finish = False
font1 = font.Font(None, 50)
font2 = font.Font(None, 20)

FPS = 60

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")

background = transform.scale(image.load(img_background), (win_width, win_height))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__ (self, img, x , y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.realod = 0
        self.rate = 10
        
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > win_height - 200:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed
        if keys[K_SPACE] and self.realod >= self.rate:
            self.realod = 0
            self.fire()
        elif self.realod < self.rate:
            self.realod += 1
    def fire(self):
        bul = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bul)
        fire.play()
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            enemy_down.play()
            self.speed = randint(1, 3)
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Button(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.clicked = False
        
    def draw(self):
        action = False
        pos = mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                
        if mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        window.blit(self.image, self.rect)
        
        return action
        
start_btn = Button(start_img, 260, 200, 150, 50, 0)      
exit_btn = Button(exit_img, 260, 255, 150, 50, 0)
restart_btn = Button(restart_img, 300, 250, 70, 25, 0)

rocket = Player(img_hero, 5, win_height - 120, 100, 100, 10)

enemys = sprite.Group()
bullets = sprite.Group()

for i in range(3):
    x = randint(80, win_width - 80)
    speed = randint(1, 3)
    enemy1 = Enemy(img_enemy1, x, -40, 60, 60, speed)
    enemys.add(enemy1)
    enemy2 = Enemy(img_enemy2, x, -200, 65, 65, speed)
    enemys.add(enemy2)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
    if finish == True:
            if restart_btn.draw():
                mixer.music.load("song.ogg")
                mixer.music.play(-1)
                
                lost = 0
                score = 0

                rocket = Player(img_hero, 5, win_height - 120, 100, 100, 10)

                enemys = sprite.Group()
                bullets = sprite.Group()

                for i in range(3):
                    x = randint(80, win_width - 80)
                    speed = randint(1, 3)
                    enemy1 = Enemy(img_enemy1, x, -40, 60, 60, speed)
                    enemys.add(enemy1)
                    enemy2 = Enemy(img_enemy2, x, -200, 65, 65, speed)
                    enemys.add(enemy2)
                finish = False

    if not finish:
        window.blit(background, (0, 0))
        if main_menu == True:
            if start_btn.draw():
                main_menu = False
            if exit_btn.draw():
                game = False
        else:
            rocket.update()
            rocket.reset()

            enemys.update()
            bullets.update()

            bullets.draw(window)
            enemys.draw(window)

            collides = sprite.groupcollide(enemys, bullets, True, True)
            for c in collides:
                shot.play()
                score += 1
                x = randint(80, win_width - 80)
                speed = randint(1, 3)
                enemy1 = Enemy(img_enemy1, x, -440, 60, 60, speed)
                enemys.add(enemy1) 
                enemy2 = Enemy(img_enemy2, x, -600, 65, 65, speed)
                enemys.add(enemy2)
  
            if sprite.spritecollide(rocket, enemys, False) or lost >= 10:
                mixer.music.load('game_over.wav')
                mixer.music.play(1)
                finish = True
                lose = font1.render("YOU LOSE!!", True, (200, 50, 50))
                window.blit(lose, (250, 215))
                    
            if score >= 30:
                mixer.music.load('game_won.wav')
                mixer.music.play(1)
                finish = True
                winner = font1.render("YOU WIN!!", True, (0, 255, 0))
                window.blit(winner, (250, 215))
        
            text_score = font2.render(f"Рахунок: {score}", True, (255, 255, 255))
            window.blit(text_score, (10, 20))

            text_score = font2.render(f"Пропущено: {lost}", True, (255, 255, 255))
            window.blit(text_score, (10, 40))
            
        if finish == True:
            if restart_btn.draw():
                finish = False
    
        display.update()
    clock.tick(FPS)