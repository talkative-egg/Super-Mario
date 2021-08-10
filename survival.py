# Graphics module from https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py
from cmu_112_graphics import *

import math, random

# Distance formula, helper function
def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** (1/2)

###################
# Mario
###################

class Mario(object):

    sprites = []

    width = 34
    height = 32
    
    # Initalizes the sprites for Mario
    @staticmethod
    def initialize(app):

        # image from http://www.mariouniverse.com/sprites-nes-smb/
        mario = app.loadImage('./assets/images/mario-sprite.png')

        # Creates 12 sprites
        for i in range(12):

            x0 = 7 + (13 + 17) * i
            y0 = 0
            x1 = x0 + 17
            y1 = 16

            sprite = mario.crop((x0, y0, x1, y1))

            # resize method learned from 
            # https://www.tutorialspoint.com/how-to-resize-an-image-using-tkinter
            sprite = sprite.resize((34, 32))
            Mario.sprites.append(sprite)

    # Construtor, takes in the initial position of mario
    def __init__(self, left, top):

        # Sprites sets off to be the 
        self.spriteX = 6

        # Left and Top margin of mario relative to top and left edge of canvas
        self.left = left
        self.top = top

        # 1 for going right, -1 for going left, 0 for nothing
        self.xMotion = 0

        # 1 for going up, 0 for when falling and staying still
        self.yMotion = 0

        # Velocities in horizontal and vertical directions
        self.xVelocity = 0
        self.yVelocity = 0

        # Used for sprites
        self.facingRight = True

    # Moves mario to the right by xVelocity amount
    def moveRight(self, app):

        # Sets the initial sprite to right if it weren't
        if(self.spriteX < len(Mario.sprites) // 2 + 1):
            self.spriteX = len(Mario.sprites) // 2 + 1

        # Update Sprite
        self.spriteX += 1
        if(self.spriteX >= len(Mario.sprites)):
            self.spriteX = len(Mario.sprites) // 2 + 1

        # If character is in right margin, then move the map instead
        if(app.map.inRightMargin(self.left + Mario.width, self.xVelocity)):
            app.map.scrollMap(self.xVelocity)
        # Move the character
        else:
            self.left += self.xVelocity
        
        # Prevents from going off of map
        if self.left > app.width - Mario.width:
            self.left = app.width - Mario.width
    
    # Moves mario to the left by -xVelocity amout
    def moveLeft(self, app):

        # Sets initial sprite to left if it weren't
        if(self.spriteX >= len(Mario.sprites) // 2 + 1):
            self.spriteX = len(Mario.sprites) // 2

        # Update sprite
        self.spriteX -= 1
        if(self.spriteX < 0):
            self.spriteX = len(Mario.sprites) // 2

        # If character in left margin, move map instead
        if(app.map.inLeftMargin(self.left, self.xVelocity)):
            app.map.scrollMap(self.xVelocity)
        else:
            self.left += self.xVelocity

        # Prevents from going off of map
        if self.left < 0:
            self.left = 0

    # Does one move to character
    def move(self, app):

        # If xMotion is 1, then character is going to the right
        if self.xMotion == 1:

            self.facingRight = True

            # Sets velocity to positive
            if self.xVelocity <= 0:
                self.xVelocity = 1
            # Accelerates by 1.3 times until reaches 20
            elif self.xVelocity < 20:
                self.xVelocity *= 1.3
            # Prevents bugs
            elif self.xVelocity < 0:
                self.xVelocity = 1

            # Move to the right
            self.moveRight(app)

        # If xMotion is -1, then character is going to the left
        elif self.xMotion == -1:
            
            # Face left for sprite
            self.facingRight = False

            # Sets velocity to negative
            if self.xVelocity >= 0:
                self.xVelocity = -1
            # Accelerates by 1.3 times until reaches -20
            elif self.xVelocity > -20:
                self.xVelocity *= 1.3
            # Prevents bugs
            elif self.xVelocity > 0:
                self.xVelocity = -1

            # Move to the left
            self.moveLeft(app)
        
        # If xMotion is 0, character is either not moving or slowing down
        elif self.xMotion == 0:

            # If xVelocity absolute value is lower than 0.5, stop the character
            if abs(self.xVelocity) <= 0.5:

                self.xVelocity = 0

                # Update to static sprite frame
                if self.facingRight:
                    self.spriteX = len(Mario.sprites) // 2
                else:
                    self.spriteX = len(Mario.sprites) // 2 - 1

            # Slows down by 1.15 times
            self.xVelocity /= 1.15

            # Still moves
            if self.xVelocity > 0:
                self.moveRight(app)
            elif self.xVelocity < 0:
                self.moveLeft(app)
    
    # Does one small part of jumping at a time
    def jump(self, map):

        # Sets initial yVelocity to 30 if mario were static
        if self.yVelocity == 0:
            self.yVelocity = 30

        # If character is falling below the leveled ground then set
        # character to be on the ground
        if (self.yMotion == 0 
            and self.top + self.yVelocity > map.level0 - Mario.height):

            self.top = map.level0 - Mario.height
            self.yVelocity = 0

        # If character is falling, increase top margin by yVelocity
        # Then increase falling speed by 1.35 times
        elif self.yMotion == 0:

            self.top += self.yVelocity
            self.yVelocity *= 1.35
        
        # If character is jumping, decrease top margin by yVelocity
        # Then decrease speed going up by 1.3 times
        else:

            self.top -= self.yVelocity
            self.yVelocity /= 1.3
        
        # If yVelocity is near 0, set it to 0
        if self.yVelocity < 1:

            self.yMotion = 0
    
    # Draws current frame of mario
    def drawMario(self, canvas):
        image = Mario.sprites[self.spriteX]
        canvas.create_image(self.left + Mario.width / 2, 
                            self.top + Mario.height / 2, 
                            image=ImageTk.PhotoImage(image))

###################
#  Clouds
###################

class Clouds(object):

    def __init__(self, app):

        # images from http://www.mariouniverse.com/sprites-nes-smb/
        self.cloud = (app.loadImage('./assets/images/tiles.png')
                                        .crop((8, 320, 40, 344))
                                        .resize((64, 48)))
        
        self.app = app

        # Sets up the clouds
        self.clouds = []
        self.cloudDimensions = (64, 48)
        self.initializeClouds()

    # Checks if a new cloud is too close to any of the previous ones
    def cloudsInRange(self, newX, newY):

        for (x0, y0) in self.clouds:

            if distance(x0, y0, newX, newY) < 80:

                return True
        
        return False

    # Initializes 8 clouds that are not near each other
    def initializeClouds(self):
        
        maxTop = self.app.height / 2
        maxWidth = self.app.width

        for i in range(8):

            x = random.randint(64, maxWidth - 64)
            y = random.randint(48, maxTop - 48)

            while self.cloudsInRange(x, y):
                x = random.randint(64, maxWidth - 64)
                y = random.randint(48, maxTop - 48)

            self.clouds.append((x, y))
    
    # Moves each of the clouds by xVelocity
    def moveClouds(self, xVelocity):

        # temp
        newClouds = []

        for (cx, cy) in self.clouds:

            cx = int(cx - xVelocity)

            # If clouds out of range, set the cloud to be on the other side of screen
            if cx + self.cloudDimensions[0] / 2 < 0:

                cx = int(self.app.width)
            
            elif cx - self.cloudDimensions[0] / 2 > self.app.width:

                cx = 0

            newClouds.append((cx, cy))

        self.clouds = newClouds

    # Draws the clouds
    def drawClouds(self, canvas):

        for (cx, cy) in self.clouds:
            canvas.create_image(cx, cy, 
                                image=ImageTk.PhotoImage(self.cloud))

###################
#  Ground Blocks
###################

class GroundBlocks(object):

    # constructor
    def __init__(self, app):

        self.app = app

        # For scrolling effect
        self.leftShift = 0

        # images from http://www.mariouniverse.com/sprites-nes-smb/
        self.groundBlock = (app.loadImage('./assets/images/tiles.png')
                                        .crop((0, 0, 16, 16))
                                        .resize((32, 32)))
        
        # Width of ground block
        self.blockWidth = 32
    
    def scrollBlocks(self, xVelocity):

        self.leftShift += xVelocity
        self.leftShift = self.leftShift % self.blockWidth
    
    # Draws the ground blocks
    def drawBlocks(self, canvas):

        cols = math.ceil(self.app.width / self.blockWidth) + 1
        rows = 2

        for row in range(rows):
            for col in range(cols):
                cx = self.blockWidth * (col) + 16 - self.leftShift
                cy = self.app.height - row * self.blockWidth - 16
                canvas.create_image(cx, cy, 
                                image=ImageTk.PhotoImage(self.groundBlock))


###################
#  Survival Map
###################

class Survival(object):
    
    # constructor
    def __init__(self, app):

        self.app = app
        
        # Sets left and right margin for when map scrolls
        self.margin = 150

        # Sets up the ground blocks
        self.groundBlocks = GroundBlocks(app)

        # Ground height
        self.level0 = app.height - self.groundBlocks.blockWidth * 2

        # Sets up the clouds
        self.clouds = Clouds(app)

    # Checks if character is going to be in the right margin of map
    def inRightMargin(self, right, xVelocity):
        return right + xVelocity > self.app.width - self.margin

    # Checks if character is going to be in the left margin of map
    def inLeftMargin(self, left, xVelocity):
        return left + xVelocity < self.margin

    # Scrolls the map by xVelocity
    def scrollMap(self, xVelocity):

        # Scrolls the ground blocks
        self.groundBlocks.scrollBlocks(xVelocity)

        # Moves the clouds
        self.clouds.moveClouds(xVelocity)
    

    # Draw background and everything in map
    def drawMap(self, canvas):
        canvas.create_rectangle(0, 0, self.app.width, self.app.height, 
                                fill="#5c94fc")
        self.clouds.drawClouds(canvas)
        self.groundBlocks.drawBlocks(canvas)

# Draws everything in survival mode
def survival_redrawAll(app, canvas):
    app.map.drawMap(canvas)
    app.mario.drawMario(canvas)

# Controller
def survival_timerFired(app):

    # Moves if mario should be moving
    if app.mario.xMotion != 0 or app.mario.xVelocity != 0:
        app.mario.move(app)
    
    # Jump if mario should be jumping
    if app.mario.yMotion != 0 or app.mario.yVelocity != 0:
        app.mario.jump(app.map)

# Controller
def survival_keyPressed(app, event):

    print("key pressed")

    if event.key == 'Right':

        # If character already has x motion, return
        if app.mario.xMotion != 0: return

        # Set x motion to right
        app.mario.xMotion = 1

    elif event.key == 'Left':

        # If character already has x motion, return
        if app.mario.xMotion != 0: return

        # Set x motion to left
        app.mario.xMotion = -1

    elif event.key == 'Up':
        
        # If character already has y motion, return
        if app.mario.yVelocity != 0: return

        app.mario.yMotion = 1

# Released motion for x
def survival_keyReleased(app, event):

    print("key released")

    if event.key == 'Right' or event.key == 'Left':
        
        app.mario.xMotion = 0

# Model
def appStarted(app):

    # Starts off in title screen
    app.mode = "titleScreen"
    app.timerDelay = 20

# Draws title screen
def titleScreen_redrawAll(app, canvas):

    canvas.create_rectangle(0, 0, app.width, app.height, fill="#5c94fc")
    canvas.create_text(app.width / 2, app.height / 3,
                       text = "Super Mario Bros!", font = "Helvetica 50")
    canvas.create_text(app.width / 2, app.height * 2 / 3,
                       text = "Press Left Arrow to play Classic Mode, refer to map1-1.py for now\n\
                               Press Right Arrow to play Survival Mode",
                       font = "Helvetica 30")

# Goes into different modes when keys pressed
def titleScreen_keyPressed(app, event):

    if event.key == "Left":
        app.mode = "classic"
    elif event.key == "Right":
        app.mode = "survival"
        app.map = Survival(app)
        Mario.initialize(app)
        app.mario = Mario(80, 385)

runApp(width=1280, height=480)