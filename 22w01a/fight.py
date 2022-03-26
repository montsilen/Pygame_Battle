import pygame, sys

screenSize = (800, 400)

pygame.init() 
displaySurface = pygame.display.set_mode(screenSize)
pygame.display.set_caption("格斗")

back = pygame.image.load("./back.jpg")
back = pygame.transform.scale(back, (800, 400))
log = pygame.image.load("./log.png")
brick = pygame.image.load("./brick.png")
man = pygame.image.load("./man.jpg")
man = pygame.transform.scale(man, (32, 32))

FPS = 60
fpsClock = pygame.time.Clock()

displaySurface.blit(back, (0, 0))
for i in range(10):
    displaySurface.blit(log, (i*16+200, 200))
for i in range(10):
    displaySurface.blit(log, (i*16+500, 200))
for i in range(10):
    displaySurface.blit(log, (i*16+100, 400))
for i in range(10):
    displaySurface.blit(log, (i*16+400, 400))
for i in range(50):
    for j in range(5):
        displaySurface.blit(brick, (i*16, 400-16-16*j))

v = 3
x = 200
y = 320
vx = 0
vy = 0
jp = 0
g  = 1
downs = [False, False, False, False]

while True:
    displaySurface.blit(back, (0, 0))
    for i in range(10):
        displaySurface.blit(log, (i*16+200, 200))
    for i in range(10):
        displaySurface.blit(log, (i*16+500, 200))
    for i in range(10):
        displaySurface.blit(log, (i*16+100, 100))
    for i in range(10):
        displaySurface.blit(log, (i*16+400, 100))
    for i in range(50):
        for j in range(5):
            displaySurface.blit(brick, (i*16, 400-16-16*j))

    displaySurface.blit(man, (x-16, y-32))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                downs[3] = True
            elif event.key == pygame.K_a:
                downs[2] = True
            elif event.key == pygame.K_w:
                downs[0] = True
            elif event.key == pygame.K_s:
                downs[1] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                downs[3] = False
            elif event.key == pygame.K_a:
                downs[2] = False
            elif event.key == pygame.K_w:
                downs[0] = False
            elif event.key == pygame.K_s:
                downs[1] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and jp in [0, 1]:
                jp += 1
                vy = -4*v
            if event.key == pygame.K_s and jp == 0:
                jp += 1
                y = y + 11
    
    vx = 0

    vx += v if downs[3] else 0
    vx -= v if downs[2] else 0
    
    if jp in [1, 2]:
        vy += g

    if 190 <= y <= 210 and vy >= 0 and 200<=x<=360:
        y = 200
        jp = 0
        vy = 0
    elif 190 <= y <= 210 and vy >= 0 and 500<=x<=660:
        y = 200
        jp = 0
        vy = 0
    elif 190 <= y <= 210 and vy >= 0 and jp == 0:
        jp = 1

    if 90 <= y <= 110 and vy >= 0 and 100<=x<=260:
        y = 100
        jp = 0
        vy = 0
    elif 90 <= y <= 110 and vy >= 0 and 400<=x<=560:
        y = 100
        jp = 0
        vy = 0
    elif 90 <= y <= 110 and vy >= 0 and jp == 0:
        jp = 1

    if x<16 and vx <0:
        vx = 0
    if x>784 and vx > 0:
        vx = 0
    
    if y >= 310 and vy >= 0:
        jp = 0
        vy = 0
        y= 320

    x += vx
    y += vy
    pygame.display.update()
    fpsClock.tick(FPS)
