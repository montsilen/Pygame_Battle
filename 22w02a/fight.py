import pygame, os.path, sys

# Create entity
class entity():
    def __init__(self, width, height, collideable, gravity, speed, name, path):
        self.width = width
        self.height = height
        self.collideable = collideable
        self.gravity = gravity
        self.speed = speed # Set the entity's maximum speed in pixels
        self.vx = 0 
        self.vy = 0 # The beginning speed is 0
        self.name = name # Set the entity's name
        self.path = path # Set the path of entity's images 
        self.imagelist = [] # Create a list for images
        for i in os.listdir("./{}".format(path)): # Search all image files in the path
            self.imagelist.append(pygame.transform.scale(pygame.image.load("./{}/{}".format(path, i)), (self.width, self.height)))  # Load all image files
        self.imagenum = 0 # Set numbers for the images loaded
        self.maxnum = len(self.imagelist) # Numbers of the numbers loaded
        self.rect = pygame.Rect(0, 0, self.width, self.height) # Create the Rect object for the entity
        entitylist.append(self) # Add this entity to the list
    def draw(self, surface):
        surface.blit(self.imagelist[self.imagenum] ,self.rect) # Draw the entity to a specific surface

# Set the most important constants of the game
SCREEN = (960, 720) # Set the size of game screen 
FPS = 60 # Set fps speed of the game
GRAVITY = 1 # Set gravity in pixels

# Init game
pygame.init() # Init Pygame
displaySurface = pygame.display.set_mode(SCREEN) # Create the main surface
pygame.display.set_caption("格斗") # Set the caption of the window
fpsClock = pygame.time.Clock()
entitylist = [] # Create a list to save all entities

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Provide exiting button
            pygame.quit() 
            sys.exit()
    
    pygame.display.update() # Draw the surface in every frame
    fpsClock.tick(FPS)