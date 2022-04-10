import pygame, sys, win32api, win32con

#Guiding Message
win32api.MessageBox(0,"玩家1（射手）： 移动：WASD；射击：C；技能：V\n玩家2（战士）： 移动：方向键；攻击：O；技能：P","操作指引",win32con.MB_OK)

# Create entity
class entity():
    def __init__(self, posx, posy, width, height, collide, gravity, side, speed, path, maxblood, dmg=0, life=True, aoe=False, time=-1):
        if not 0 in entitylist:
            self.id = len(entitylist)
            entitylist.append(self)
        else:
            self.id = entitylist.index(0)
            entitylist[self.id] = self
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.collide = collide # True, False
        self.gravity = gravity # True, False
        self.side = side # 0: neutral, 1: player1, 2: player2
        self.speed = speed # Set the entity's maximum speed in pixels
        self.vx = 0 
        self.vy = 0 # The beginning speed is 0
        self.blood = maxblood
        self.maxblood = maxblood
        self.life = life
        self.dmg = dmg
        self.path = path # Set the path of entity's images 
        self.useimg = 0, 0
        self.images = pygame.image.load("./img/{}".format(path))
        sizex, sizey = self.images.get_rect().size
        self.blocks = sizex//width, sizey//height
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height) # Create the Rect object for the entity
        self.dmged = []
        self.aoe = aoe
        self.time = time

    def draw(self, surface):
        surface.blit(self.images, (self.posx, self.posy+PULLDOWN), (self.useimg[0]*self.width, self.useimg[1]*self.height, self.width, self.height))
    
    def update(self, maps, flag=False): # Calculate the entity's information of the next frame
        if flag:
            flags = 0
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.vy += GRAVITY if self.gravity else 0
        if self.collide:
            col = self.collidemap(maps)
            if col[0] == 1:
                self.destroy()
                if flag:
                    flags = 1
            elif col[0] == 2:
                self.setpos(self.posx, col[1]-self.height)
                self.setspeed(self.vx, 0)
                if flag:
                    flags = 2
        self.collideborder(WIDTH*16, HEIGHT*16, not self.life)
        self.posx += self.vx
        self.posy += self.vy
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        if flag:
            return flags
        

    def imgchange(self, pause, destroy=False):
        if self.useimg[0] < self.blocks[0]:
            self.useimg[0] += 1
        else:
            self.useimg[1] += 1
            self.useimg[2] += 0

    def setspeed(self, vx, vy):
        self.vx = vx
        self.vy = vy
    
    def addtospeed(self, dvx, dvy):
        self.vx += dvx
        self.vy += dvy
    
    def setpos(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def collidemap(self, maps, destory=False):
        cx, cy = self.rect.midbottom
        if cy >= int(maps[0])*16 and self.vy >= 0: 
            if destory:
                return 1, 0
            return 2, int(maps[0])*16
        for i in range(1, len(maps)):
            height, start, end = map(int, maps[i].split())
            if start*16 <= cx <= end*16 and height*16-8 < cy < height*16+16 and self.vy >= 0:
                if destory:
                    return 1, 0
                return 2, height*16
        return 0, 0

    def collideborder(self, screenW, screenH, destroy=False):
        left = self.rect.left
        right = self.rect.right
        top = self.rect.top
        bottom = self.rect.bottom
        if destroy:
            if left > screenW or bottom < 0 or right < 0 or top > screenH:
                self.destroy()
        else:
            if right > screenW:
                self.setspeed(0, self.vy)
                self.setpos(screenW-self.width, self.posy)
            if left < 0:
                self.setspeed(0, self.vy)
                self.setpos(0, self.posy)
            if top < 0:
                self.setspeed(self.vx, 0)
                self.setpos(self.posx, 0)

    def collideentity(self, entityc):
        if self.rect.colliderect(entityc.rect):
            if self.side != entityc.side and not entityc.id in self.dmged:
                entityc.blood -= self.dmg
                self.dmged.append(entityc.id)
                dmglist.append([self.dmg, self.posx, self.posy+PULLDOWN, 0])
                if not self.aoe:
                    self.destroy()

    def destroy(self):
        global entitylist
        entitylist[self.id] = 0

# Set player as a class and its main keyboard actions
JUMP = "jump"
LEFT = "left"
RIGHT = "right"
DOWN = "down"
SHOOT = "shoot"
CHOP = "chop"
ABLE1 = "able1"
class player(entity):
    def __init__(self, posx, posy, width, height, side, speed, path, blood, faceright=True, entityc=0):
        super().__init__(posx, posy, width, height, True, True, side, speed, path, blood)
        self.jumpspeed = self.speed*3
        self.airstatus = 0
        self.face = faceright
        self.count0 = 0
        self.cd0 = 0
        self.count1 = 0
        self.cd1 = 0
        self.attachment = entityc
        self.attcount = 0

    def setCDcounter(self, cd0, cd1):
        self.cd1 = cd1
        self.cd0 = cd0

    def update(self, maps):
        col = super().update(maps, True)
        if self.vx > 0:
            self.face = True
        elif self.vx < 0:
            self.face = False
        if self.vx < 0:
            self.useimg = 0, 2
        elif self.vx > 0:
            self.useimg = 0, 0
        else:
            self.useimg = 0, 1
        if col == 2:
            self.airstatus = 0
        if self.count0 > 0:
            self.count0 -= 1
        if self.count1 > 0:
            self.count1 -= 1
        if self.attachment:
            if self.attcount > 0:
                self.attcount -= 1
            if self.face:
                self.attachment.posx = self.posx + 24
                self.attachment.posy = self.posy + 4
            else:
                self.attachment.posx = self.posx - 8
                self.attachment.posy = self.posy + 4
            if self.face and self.attcount:
                self.attachment.useimg = 0, self.attcount//4
            elif not self.face and self.attcount:
                self.attachment.useimg = 1, self.attcount//4
            elif self.face and not self.attcount:
                self.attachment.useimg = 0, 2
            elif not self.face and not self.attcount:
                self.attachment.useimg = 1, 2
            if self.attcount == 0:
                self.attachment.dmged = list(range(len(entitylist)))

    def action(self, action, maps):
        if action == LEFT:
            self.addtospeed(-self.speed, 0)
        elif action == RIGHT:
            self.addtospeed(self.speed, 0)
        elif action == JUMP and self.airstatus in [0, 1]:
            self.airstatus += 1
            self.setspeed(self.vx, -self.jumpspeed)
        elif action == DOWN:
            if self.collidemap(maps)[0] == 2:
                self.setpos(self.posx, self.posy+17)
                self.airstatus = 1
        elif action == SHOOT and self.count0 == 0:
            if self.face:
                a = entity(self.posx+16, self.posy+8, 16, 16, False, False, self.side, 12, "bullet.png", 0, 245, False)
                a.setspeed(12, 0)
            else:
                a = entity(self.posx, self.posy+8, 16, 16, False, False, self.side, 12, "bullet.png", 0, 245, False)
                a.setspeed(-12, 0)
                a.useimg = 0, 2
            self.count0 = self.cd0
        elif action == ABLE1 and self.count1 == 0:
            a = entity(self.posx+16, self.posy+8, 16, 16, False, False, self.side, 12, "bullet.png", 0, 245, False, True)
            a.setspeed(12, 0)
            a = entity(self.posx, self.posy+8, 16, 16, False, False, self.side, 12, "bullet.png", 0, 245, False, True)
            a.setspeed(-12, 0)
            a.useimg = 0, 2
            a = entity(self.posx+8, self.posy, 16, 16, False, False, self.side, 12, "bullet.png", 0, 245, False, True)
            a.setspeed(0, -12)
            a.useimg = 0, 1
            a = entity(self.posx+8, self.posy+16, 16, 16, False, False, self.side, 12, "bullet.png", 0, 245, False, True)
            a.setspeed(0, 12)
            a.useimg = 0, 3
            self.count1 = self.cd1
        elif action == CHOP and self.count0 == 0:
            self.attachment.dmged = []
            self.count0 = self.cd0
            self.attcount = 20

# Set the most important constants of the game
WIDTH = 60
HEIGHT = 35
PULLDOWN = 32
SCREEN = WIDTH*16, HEIGHT*16+PULLDOWN
PLAYSCREEN = WIDTH*16, HEIGHT*16 # Set the size of game screen 
FPS = 60 # Set fps speed of the game
GRAVITY = 1 # Set gravity in pixels

# Init pygame module
pygame.init() # Init Pygame
displaySurface = pygame.display.set_mode(SCREEN) # Create the main surface
pygame.display.set_caption("格斗") # Set the caption of the window
fpsClock = pygame.time.Clock()
entitylist = [] # Create a list to save all entities

# Import map
brickImg = pygame.image.load("brick.png")
logImg = pygame.image.load("log.png")
def importMap(path):
    mapfile = open(path, "rt")
    maplist = mapfile.readlines()
    mapfile.close()
    return maplist

def drawMap(maplist, surface):
    for i in range(int(maplist[0]), HEIGHT):
        for j in range(WIDTH):
            surface.blit(brickImg, (16*j, 16*i))
    for i in range(1, len(maplist)):
        height, start, end  = map(int, maplist[i].split())
        for j in range(start, end):
            surface.blit(logImg, (j*16, height*16))

# Blood stripes and damage
numberimg1 = pygame.image.load("./numbers1.png").convert_alpha()
numberimg2 = pygame.image.load("./numbers2.png").convert_alpha()
def drawnumbers(numbers, type):
    if type == 1:
        surface = pygame.Surface((10*len(numbers)-2, 16)).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for i in range(len(numbers)):
            if numbers[i] == "/":
                surface.blit(numberimg1, (i*10, 0), (80, 0, 8, 16))
            else:
                surface.blit(numberimg1, (i*10, 0), (int(numbers[i])*8, 0, 8, 16))
        return surface
    if type == 2:
        surface = pygame.Surface((8*len(numbers)-2, 13)).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for i in range(len(numbers)):
            surface.blit(numberimg2, (i*8, 0), (int(numbers[i])*6, 0, 6, 13))
        return surface

def initHp():
    hpSurface.fill((100, 100, 100))
    font = pygame.font.SysFont("Arial", 24) 
    p1 = font.render("Player1", True, (255, 200, 10), (100, 100, 100))
    p2 = font.render("Player2", True, (255, 200, 10), (100, 100, 100))
    vs = font.render("VS", True, (255, 200, 10), (100, 100, 100))
    r1 = p1.get_rect()
    r1.left = 5
    r1.centery = 16
    r2 = p2.get_rect()
    r2.right = SCREEN[0] - 5
    r2.centery = 16
    rvs = vs.get_rect()
    rvs.center = SCREEN[0]//2, 16
    hpSurface.blit(p1, (5, 0))
    hpSurface.blit(p2, r2)
    hpSurface.blit(vs, rvs)
    w = (SCREEN[0] - 2*r1.width - rvs.width - 50)//2
    pygame.draw.rect(hpSurface, (255, 255, 255), (r1.width+15, 4, w, 24), 0)
    pygame.draw.rect(hpSurface, (255, 255, 255), (SCREEN[0]-r1.width-15-w, 4, w, 24), 0)
    return w, r1.width

def drawHp(surface, p1, p2, w, s, p):
    b1 = int(p1.blood/p1.maxblood*w)
    b2 = int(p2.blood/p2.maxblood*w)
    if b1 > 0:
        pygame.draw.rect(surface, (255, 0, 0), (s+15, 4, b1, 24), 0)
        w1 = drawnumbers("{}/{}".format(p1.blood, p1.maxblood), 1)
        r1 = w1.get_rect()
        r1.center = (p, 16)
        surface.blit(w1, r1)
    if b2 > 0:
        pygame.draw.rect(surface, (255, 0, 0), (SCREEN[0]-s-15-b2, 4, b2, 24), 0)
        w2 = drawnumbers("{}/{}".format(p2.blood, p2.maxblood), 1)
        r2 = w2.get_rect()
        r2.center = (SCREEN[0]-p, 16)
        surface.blit(w2, r2)

dmglist = []

def drawDmg(surface):
    for i in dmglist:
        i[2] -= 1
        i[3] += 1
        if i[3] < 30:
            dmg = drawnumbers(str(i[0]), 2)
            surface.blit(dmg, (i[1], i[2]))

# Settings
maplist = importMap("map.txt")

# Subsurfaces
mapSurface = pygame.Surface(SCREEN)
hpSurface = pygame.Surface((SCREEN[0], PULLDOWN))

# Init game
mapSurface.blit(pygame.transform.scale(pygame.image.load("back.jpg"), SCREEN), (0, 0))
drawMap(maplist, mapSurface)
stripeWidth, wordWidth = initHp()
place = wordWidth+15 + stripeWidth//2

# test
player1 = player(0, 0, 32, 32, 1, 4, "man1.png", 4620)
player2 = player(SCREEN[0], 0, 32, 32, 2, 4, "man2.png", 4620, True)
sword = entity(0, 0, 16, 16, False, False, 2, 0, "sword.png", 0, 335, False, True)
player2.attachment = sword

player1.setCDcounter(25, 90)
player2.setCDcounter(25, 90)

while True:
    print(entitylist)
    player1.setspeed(0, player1.vy)
    player2.setspeed(0, player2.vy)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Provide exiting button
            pygame.quit() 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.action(JUMP, maplist)
            if event.key == pygame.K_s:
                player1.action(DOWN, maplist)
            if event.key == pygame.K_c:
                player1.action(SHOOT, maplist)
            if event.key == pygame.K_v:
                player1.action(ABLE1, maplist)
            if event.key == pygame.K_UP:
                player2.action(JUMP, maplist)
            if event.key == pygame.K_DOWN:
                player2.action(DOWN, maplist)
            if event.key == pygame.K_o:
                player2.action(CHOP, maplist)
            if event.key == pygame.K_p:
                player2.action(ABLE1, maplist)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player1.action(LEFT, maplist)
    if keys[pygame.K_d]:
        player1.action(RIGHT, maplist)
    if keys[pygame.K_LEFT]:
        player2.action(LEFT, maplist)
    if keys[pygame.K_RIGHT]:
        player2.action(RIGHT, maplist)
    
    displaySurface.blit(mapSurface, (0, PULLDOWN))
    for i in entitylist:
        if i:
            i.update(maplist)
            i.draw(displaySurface)
    for i in range(2, len(entitylist)):
        if entitylist[i]:
            entitylist[i].collideentity(player1)
        if entitylist[i]:
            entitylist[i].collideentity(player2)

    displaySurface.blit(hpSurface, (0, 0))
    drawHp(displaySurface, player1, player2, stripeWidth, wordWidth, place)
    drawDmg(displaySurface)
    
    pygame.display.update() # Draw the surface in every frame
    fpsClock.tick(FPS)