from pygame import *
from random import randint
font.init()


mixer.init()

WALL_COLOR = (100,0,255)
clock = time.Clock()
FPS = 60
W, H = ( 700, 500 )
P_SIZE = (75,75)
E_SIZE = (75,75)
G_SIZE = (60,60)

window = display.set_mode((W, H))
display.set_caption('Догонялки')
background = transform.scale(image.load('background.jpg'),(W, H))
mixer.music.load('jungles.ogg')
kick = mixer.Sound('kick.ogg')

money = mixer.Sound('money.ogg')

#sprite_1 = transform.scale(image.load('cyborg.png'), (100,100))

x1,y1 = 100,100
x2,y2 = 200,200

class Game():
    run = True
    finish = False
    win = False
    events = []
    key_pressed = {}
    list_mousebuttondown = []

    def update(self):
        self.events = event.get()
        for e in self.events:
            if e.type == QUIT:
                self.run = False 
        self.key_pressed = key.get_pressed()

    
        for e in self.events:
            if e.type ==MOUSEBUTTONDOWN:
                self.button = e.button
                self.pos = e.pos
                for func in self.list_mousebuttondown:
                    if func[0].visibility and func[0].rect.collidepoint(*self.pos) and self.button == 1:
                        func[1]()
    def mousebuttondown(self,obj,func):
        self.list_mousebuttondown.append([obj,func])



class GameSprite(sprite.Sprite):
    def __init__(self, imagefile, x, y, width,  height, speed):
        super().__init__()
        self.image = transform.scale(image.load(imagefile), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        if  game.key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if  game.key_pressed[K_RIGHT] and self.rect.x < W - self.rect.width:
            self.rect.x += self.speed
        if  game.key_pressed[K_DOWN] and self.rect.y < H - self.rect.height:
            self.rect.y += self.speed
        if  game.key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed


class Enemy(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= self.x2 or self.rect.x <= self.x1:
            self.speed = self.speed * -1
    def set_move(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def collide(self):
        return randint(0,1)

def create_walls(params):
    walls = []
    for p in params:
        walls.append(Wall(*p,WALL_COLOR))
    return walls

class Wall(sprite.Sprite):
    def __init__(self, x, y , width , height , color):
        super().__init__()
        self.color= color
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Button(sprite.Sprite):
    def __init__(self, x, y , width , height , bg_color, text, font_size,text_color, func = None):
        super().__init__()
        self.bg_color= bg_color
        self.image = Surface((width, height))
        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = font.SysFont('Arial', font_size)
        self.text_img = self.font.render(text, True, text_color)
        self.image.blit(self.text_img,(10,10))
        self.func = func
        self.visibility = True
        self.mousebuttondown(func)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
    
    # def update():
    #     if not self.func is None:
    #         if self.rect.collide_rect

    
    def show(self):
        self.visibility = True
    def hide(self):
        self.visibility = False    
    def mousebuttondown(self,func):
        game.mousebuttondown(self,func)
    def update(self):
        if self.visibility:
            self.reset()
    
def func_test_1():
    level_1.reset()
    game.finish = False

class Level():
    def __init__(self, walls, p_cor, e_cor, g_cor):
        self.walls = walls
        self.p_cor = p_cor
        self.e_cor = e_cor
        self.g_cor = g_cor
    
    def reset(self):
        global walls, player, enemy, gold
        walls = create_walls(params_level_1)
        player = Player('hero.png', *self.p_cor, *P_SIZE, 10)
        enemy = Enemy('cyborg.png',*self.e_cor, *E_SIZE,5)
        gold = GameSprite('treasure.png',*self.g_cor,*G_SIZE,0)
        enemy.set_move(enemy.rect.x , enemy.rect.y , 625 , 0)
        return walls, player, enemy, gold




params_level_1 = [
    (15,98,300,20),
    (400,0,20,196),
    (80,196,320,20),
    (100,216,20,200),
    (120,400,120,20),
    (375,425,20,75),
    (375,425,52,20),
    (620,220,80,20),
    (410,300,50,50),
    (500, 265, 25,25)
]
# wall_4 = Wall(150,300,20,200,WALL_COLOR)
game = Game()

level_1 = Level(params_level_1, (20,20), (350,350), (400,450))
walls, player, enemy, gold = level_1.reset()


font_1 = font.SysFont('Arial', 70)
win = font_1.render('YOU WIN!', True, (0,200,0))
lose = font_1.render('YOU LOSE!', True, (200,0,0))
button = Button(250,200,220,100,(204,102,0), 'RESET', 70, (255,253,208),func_test_1)

mixer.music.play()
mixer.music.set_volume(0.2)


while game.run:
    
    game.update()
    window.blit(background,(0,0))
    
    if game.finish != True:
        enemy.update()
        player.update()

        for w in walls:
            w.reset()
            if sprite.collide_rect(player,w):
                game.win = False
                game.finish = True
                kick.play()
        
        if sprite.collide_rect(player,enemy):
            game.win = False
            game.finish = True
            kick.play()
        
        if sprite.collide_rect(player,gold):
            game.win = True
            game.finish = True
            money.play()
            
    else:
        if game.win:
            window.blit(win,(200,100))
        else:
            window.blit(lose,(200,100))
    if game.finish == True:
        button.reset()
        


    
    player.reset()
    enemy.reset()
    gold.reset()


    


    display.update()
    clock.tick(FPS)

