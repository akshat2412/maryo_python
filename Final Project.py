import pygame,sys,random
from pygame.locals import *
pygame.init()

#variables
window_width=1200
window_height=600
black=(0,0,0)
white=(255,255,255)
no_of_fireballs=0
fireballs_list=[]
fireball_limit=15
score=0
score_update=0
level=1
topscore=0

#creating gamescreen
mainclock=pygame.time.Clock()
canvas=pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Maryo')
canvas.fill(black)
pygame.display.update()


font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)
gamestart=pygame.mixer.Sound('mario_theme.wav')
gameover=pygame.mixer.Sound('mario_dies.wav')

class flames:
    def __init__(self):
        self.image_flames = pygame.image.load('fire_bricks.png')
        self.image_flames_rect = self.image_flames.get_rect()
        self.image_flames_rect.top = 550
        canvas.blit(self.image_flames, self.image_flames_rect)

    def render_flames_image(self):
        canvas.blit(self.image_flames, self.image_flames_rect)

    def update_flames(self):
        self.image_flames_rect.top -= 50

class cactus:
    def __init__(self):
        self.image_cactus = pygame.image.load('cactus_bricks.png')
        self.image_cactus_rect = self.image_cactus.get_rect()
        self.image_cactus_rect.top = -150
        canvas.blit(self.image_cactus, self.image_cactus_rect)

    def render_cactus_image(self):
        canvas.blit(self.image_cactus, self.image_cactus_rect)

    def update_cactus(self):
        self.image_cactus_rect.top+=50

class maryo(cactus, flames):
    def __init__(self):
        self.pos_y = 300
        self.pos_y_change = 18
        self.image = pygame.image.load('pco5xxecE.png')
        self.image = pygame.transform.scale(self.image,(40,40))
        self.image_rect = self.image.get_rect()
        self.image_rect.top = self.pos_y
        self.image_rect.left = 50
        canvas.blit(self.image, self.image_rect)
        self.score_change=0
        self.top_score=0

    def movement(self, event):
         if event.type == pygame.KEYDOWN:
             if event.key == K_UP:
                 self.pos_y_change = -18
         if event.type == pygame.KEYUP:
             if event.key == K_UP:
                 self.pos_y_change = 18

    def score_update(self,event):
         if event.type == pygame.KEYDOWN:
             if event.key == K_UP:
                 self.score_change=1
         if event.type == pygame.KEYUP:
             if event.key == K_UP:
                 self.score_change=0
         return self.score_change

    def render_player_image(self):
        self.pos_y += self.pos_y_change
        self.image_rect.top = self.pos_y
        canvas.blit(self.image, self.image_rect)

class dragon(cactus, flames):
    def __init__(self):
        self.pos_y = 300
        self.pos_y_change = -25
        self.image = pygame.image.load('dragon.png')
        self.image_rect = self.image.get_rect()
        self.image_rect.top = self.pos_y
        self.image_rect.right = 1180
        canvas.blit(self.image, self.image_rect)

    def movement_and_render(self):
        if self.image_rect.top<=cactus.image_cactus_rect.bottom:
            self.pos_y_change=25
        elif self.image_rect.bottom>=550:
            self.pos_y_change=-25
        self.image_rect.top+=self.pos_y_change
        canvas.blit(self.image, self.image_rect)

class fireballs(dragon):

    def __init__(self):
        self.image_fireballs = pygame.image.load('fireball.png')
        self.image_fireballs = pygame.transform.scale(self.image_fireballs,(20,20))
        self.image_fireballs_rect = self.image_fireballs.get_rect()
        self.image_fireballs_rect.centery = dragon.image_rect.centery
        self.image_fireballs_rect.centerx = dragon.image_rect.centerx - 5
        canvas.blit(self.image_fireballs, self.image_fireballs_rect)


    def update_fireballs(self):
        self.image_fireballs_rect.left-=30
        canvas.blit(self.image_fireballs,self.image_fireballs_rect)

    def checklimit(self):
        if(self.image_fireballs_rect).left<=0:
            return True
        return False


def check_boundary_collision(maryo,cactus,flames):
    if maryo.image_rect.top<=cactus.image_cactus_rect.bottom-12 or maryo.image_rect.bottom>=flames.image_flames_rect.top+29:
        return True
    return False

def check_fireball_collision(fireballs_obj,player):
    if player.image_rect.colliderect(fireballs_obj.image_fireballs_rect):
        return True
    return False

def level_update(score):
    if score in range(0,250):
        level=1
    elif score in range (250,500):
        level=2
    elif score in range (500,750):
        level=3
    else:
        level=4
    return level

def drawtext(text, font, surface, x, y):        #to display text on the screen
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

#game objects


pygame.display.update()

#game variables
game=True
startscreen=True
gameplay=False
endscreen=False


#game objects
player = maryo()
cactus = cactus()
flames = flames()
dragon = dragon()


while game:
    gameover.stop()
    gamestart.play(-1,0)
    while startscreen:
        image_start=pygame.image.load('start.png')
        image_start_rect=image_start.get_rect()
        image_start_rect.centerx=600
        image_start_rect.centery=300
        canvas.blit(image_start,image_start_rect)

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    game=False
                    gameplay=False
                    endscreen=False
                startscreen=False
                gameplay=True
        pygame.display.update()


    #main gameplay loop
    while gameplay:
        for event in pygame.event.get():
            if event.key == K_ESCAPE:
                game = False
                gameplay = False
                endscreen = False
            player.movement(event)
            score_update=player.score_update(event)

        score += score_update
        if level != level_update(score):
            cactus.update_cactus()
            flames.update_flames()
            fireball_limit-=4
            level=level_update(score)

        canvas.fill(black)
        cactus.render_cactus_image()
        flames.render_flames_image()
        player.render_player_image()
        dragon.movement_and_render()
        if(topscore<=score):
            topscore=score
        drawtext('Score : %s | Top Score : %s | Level %s' % (score,topscore,level),scorefont,canvas,350,cactus.image_cactus_rect.bottom+10)

        #loop for creating fireballs
        no_of_fireballs+=1
        if no_of_fireballs>=fireball_limit:
            newfireball=fireballs()
            fireballs_list.append(newfireball)
            no_of_fireballs=0

        for i in fireballs_list:
            fireballs.update_fireballs(i)
            if check_fireball_collision(i,player):
                gameplay=False
                endscreen=True
            if fireballs.checklimit(i):
                fireballs_list.remove(i)

        if check_boundary_collision(player,cactus,flames):
            gameplay=False
            endscreen=True

        pygame.display.update()
        mainclock.tick(15)

    gamestart.stop()
    gameover.play(0)
    #game over screen loop
    while endscreen:

        image_end=pygame.image.load('end.png')
        image_end_rect=image_end.get_rect()
        image_end_rect.centerx = 600
        image_end_rect.centery = 300
        canvas.fill(black)
        canvas.blit(image_end, image_end_rect)
        canvas.blit(player.image,player.image_rect)
        canvas.blit(flames.image_flames,flames.image_flames_rect)
        canvas.blit(cactus.image_cactus,cactus.image_cactus_rect)
        canvas.blit(dragon.image,dragon.image_rect)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    game = False
                gameplay=True
                endscreen = False
                player.image_rect.top=300
                player.image_rect.left=50
                player.pos_y=300
                player.pos_y_change=18
                cactus.image_cactus_rect.top = -150
                flames.image_flames_rect.top = 550
                score=0
                level=1
                no_of_fireballs=0
                fireballs_list.clear()
        pygame.display.update()


pygame.quit()
quit()
