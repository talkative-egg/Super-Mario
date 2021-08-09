from cmu_112_graphics import *

import math, random

def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** (1/2)

###################
# Mario
###################

class Mario(object):

    sprites = []

    width = 34
    height = 32
    
    @staticmethod
    def initialize(app):

        mario = app.loadImage('./assets/images/mario-sprite.png')

        for i in range(12):

            x0 = 7 + (13 + 17) * i
            y0 = 0
            x1 = x0 + 17
            y1 = 16

            sprite = mario.crop((x0, y0, x1, y1))
            sprite = sprite.resize((34, 32))
            Mario.sprites.append(sprite)

    def __init__(self, left, top):
        self.spriteX = 6
        self.spriteY = 0
        self.left = left
        self.top = top
        self.xMotion = 0
        self.yMotion = 0
        self.xVelocity = 0
        self.yVelocity = 0
        self.facingRight = True

    def moveRight(self, app):
        if(self.spriteX < len(Mario.sprites) // 2 + 1):
            self.spriteX = len(Mario.sprites) // 2 + 1

        self.spriteX += 1
        if(self.spriteX >= len(Mario.sprites)):
            self.spriteX = len(Mario.sprites) // 2 + 1

        if(app.map.inRightMargin(self.left + Mario.width, self.xVelocity)):
            app.map.scrollMap(self.xVelocity)
        else:
            self.left += self.xVelocity
        
        if self.left > app.width - Mario.width:
            self.left = app.width - Mario.width
    
    def moveLeft(self, app):
        if(self.spriteX >= len(Mario.sprites) // 2 + 1):
            self.spriteX = len(Mario.sprites) // 2

        self.spriteX -= 1
        if(self.spriteX < 0):
            self.spriteX = len(Mario.sprites) // 2

        if(app.map.inLeftMargin(self.left, self.xVelocity)):
            app.map.scrollMap(self.xVelocity)
        else:
            self.left += self.xVelocity

        if self.left < 0:
            self.left = 0

    def move(self, app):

        if self.xMotion == 1:

            self.facingRight = True

            if self.xVelocity == 0:
                self.xVelocity = 1
            elif self.xVelocity < 20:
                self.xVelocity *= 2

            self.moveRight(app)

        elif self.xMotion == -1:
            
            self.facingRight = False

            if self.xVelocity == 0:
                self.xVelocity = -1
            elif self.xVelocity > -20:
                self.xVelocity *= 1.2

            self.moveLeft(app)
        
        elif self.xMotion == 0:

            if abs(self.xVelocity) <= 1:

                self.xVelocity = 0

                if self.facingRight:
                    self.spriteX = len(Mario.sprites) // 2
                else:
                    self.spriteX = len(Mario.sprites) // 2 - 1

            self.xVelocity /= 1.25

            if self.xVelocity > 0:
                self.moveRight(app)
            elif self.xVelocity < 0:
                self.moveLeft(app)
    
    def jump(self, map):

        if self.yVelocity == 0:
            self.yVelocity = 30

        if (self.yMotion == 0 
            and self.top + self.yVelocity > map.level0 - Mario.height):

            self.top = map.level0 - Mario.height
            self.yVelocity = 0

        elif self.yMotion == 0:

            self.top += self.yVelocity
            self.yVelocity *= 1.35
        
        else:

            self.top -= self.yVelocity
            self.yVelocity /= 1.3
        
        if self.yVelocity < 0.5:

            self.yMotion = 0
    
    def drawMario(self, app, canvas):
        image = Mario.sprites[self.spriteX]
        canvas.create_image(self.left + Mario.width / 2, 
                            self.top + Mario.height / 2, 
                            image=ImageTk.PhotoImage(image))

###################
#  Survival
###################

class Survival(object):
    
    def __init__(self, app):
        self.app = app
        self.leftShift = 0
        self.groundBlock = (app.loadImage('./assets/images/tiles.png')
                                        .crop((0, 0, 16, 16))
                                        .resize((32, 32)))
        self.cloud = (app.loadImage('./assets/images/tiles.png')
                                        .crop((8, 320, 40, 344))
                                        .resize((64, 48)))
        self.margin = 150
        self.width = app.width
        self.blockWidth = 32
        self.level0 = app.height - self.blockWidth * 2
        self.clouds = []
        self.cloudDimensions = (64, 48)
        self.initializeClouds()

    def cloudsInRange(self, newX, newY):

        for (x0, y0) in self.clouds:

            if distance(x0, y0, newX, newY) < 80:

                return True
        
        return False

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


    def updateClouds(self):

        for i in range(4):
            self.addCloud
    
    def inRightMargin(self, right, xVelocity):
        return right + xVelocity > self.width - self.margin

    def inLeftMargin(self, left, xVelocity):
        return left + xVelocity < self.margin

    def moveClouds(self, xVelocity):

        newClouds = []

        for (cx, cy) in self.clouds:

            cx = int(cx - xVelocity)

            if cx + self.cloudDimensions[0] / 2 < 0:

                cx = int(self.app.width)
            
            elif cx - self.cloudDimensions[0] / 2 > self.app.width:

                cx = 0

            newClouds.append((cx, cy))

        self.clouds = newClouds

    def scrollMap(self, xVelocity):

        self.leftShift += xVelocity
        self.leftShift = self.leftShift % self.blockWidth

        self.moveClouds(xVelocity)

    def drawBlocks(self, canvas):
        cols = math.ceil(self.app.width / self.blockWidth) + 1
        rows = 2

        for row in range(rows):
            for col in range(cols):
                cx = self.blockWidth * (col) + 16 - self.leftShift
                cy = self.app.height - row * self.blockWidth - 16
                canvas.create_image(cx, cy, 
                                image=ImageTk.PhotoImage(self.groundBlock))
    
    def drawClouds(self, canvas):

        for (cx, cy) in self.clouds:
            canvas.create_image(cx, cy, 
                                image=ImageTk.PhotoImage(self.cloud))

    def drawMap(self, canvas):
        canvas.create_rectangle(0, 0, self.app.width, self.app.height, 
                                fill="#5c94fc")
        self.drawClouds(canvas)
        self.drawBlocks(canvas)

def survival_redrawAll(app, canvas):
    app.map.drawMap(canvas)
    app.mario.drawMario(app, canvas)

def survival_timerFired(app):

    if app.mario.xMotion != 0 or app.mario.xVelocity != 0:
        app.mario.move(app)
    
    if app.mario.yMotion != 0 or app.mario.yVelocity != 0:
        app.mario.jump(app.map)

def survival_keyPressed(app, event):

    print("key pressed")

    if event.key == 'Right':

        if app.mario.xMotion != 0: return

        app.mario.xMotion = 1

    elif event.key == 'Left':

        if app.mario.xMotion != 0: return

        app.mario.xMotion = -1

    elif event.key == 'Up':
        
        app.mario.yMotion = 1

def survival_keyReleased(app, event):

    print("key released")

    if event.key == 'Right' or event.key == 'Left':
        
        app.mario.xMotion = 0

def appStarted(app):
    app.mode = "titleScreen"
    app.timerDelay = 20

def titleScreen_redrawAll(app, canvas):

    canvas.create_rectangle(0, 0, app.width, app.height, fill="#5c94fc")
    canvas.create_text(app.width / 2, app.height / 3,
                       text = "Super Mario Bros!", font = "Helvetica 50")
    canvas.create_text(app.width / 2, app.height * 2 / 3,
                       text = "Press Left Arrow to play Classic Mode\n\
                               Press Right Arrow to play Survival Mode",
                       font = "Helvetica 30")

def titleScreen_keyPressed(app, event):
    if event.key == "Left":
        app.mode = "classic"
    elif event.key == "Right":
        app.mode = "survival"
        app.map = Survival(app)
        Mario.initialize(app)
        app.mario = Mario(80, 385)

runApp(width=1280, height=480)