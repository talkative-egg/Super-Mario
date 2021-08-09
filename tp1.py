from cmu_112_graphics import *

import math

class Map(object):

    imageWidth = 640
    imageHeight = 240
    width = 1280
    height = 480
    margin = 500

    def __init__(self, app, path):
        self.x0 = 0
        self.y0 = 0
        self.width = 3584
        self.image = app.loadImage(path)
    
    def drawMap(self, app, canvas):

        display = (self.image.crop((self.x0, self.y0, 
                                    self.x0 + Map.imageWidth, 
                                    self.y0 + Map.imageHeight))
                             .resize((Map.width, Map.height)))

        canvas.create_image(app.width / 2, app.height / 2, 
                            image=ImageTk.PhotoImage(display))
    
    def inMargin(self, right, dx):

        if self.x0 + Map.imageWidth + dx >= self.width:
            return False

        return right > Map.width - Map.margin
    
    def scrollMap(self, dx):
        self.x0 += dx

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
        self.xVelocity = 0
        self.yVelocity = 0

    def moveRight(self, app):
        if(self.spriteX < len(Mario.sprites) // 2 + 1):
            self.spriteX = len(Mario.sprites) // 2 + 1

        self.spriteX += 1
        if(self.spriteX >= len(Mario.sprites)):
            self.spriteX = len(Mario.sprites) // 2 + 1

        if(app.map.inMargin(self.left + Mario.width, self.xVelocity)):
            app.map.scrollMap(self.xVelocity)
        else:
            self.left += self.xVelocity
        
        if self.left > app.width - Mario.width:
            self.left = app.width - Mario.width
    
    def moveLeft(self):
        if(self.spriteX >= len(Mario.sprites) // 2 + 1):
            self.spriteX = len(Mario.sprites) // 2

        self.spriteX -= 1
        if(self.spriteX < 0):
            self.spriteX = len(Mario.sprites) // 2

        self.left += self.xVelocity

        if self.left < 0:
            self.left = 0

    def move(self, app):

        if self.xMotion == 1:

            if self.xVelocity == 0:
                self.xVelocity = 1
            elif self.xVelocity < 20:
                self.xVelocity *= 2

            self.moveRight(app)

        elif self.xMotion == -1:

            if self.xVelocity == 0:
                self.xVelocity = -1
            elif self.xVelocity > -20:
                self.xVelocity *= 2

            self.moveLeft()
        
        elif self.xMotion == 0:

            if abs(self.xVelocity) <= 1:
                self.xVelocity = 0

            self.xVelocity /= 1.25

            if self.xVelocity > 0:
                self.moveRight(app)
            elif self.xVelocity < 0:
                self.moveLeft()
    
    def drawMario(self, app, canvas):
        image = Mario.sprites[self.spriteX]
        canvas.create_image(self.left + Mario.width / 2, 
                            self.top + Mario.height / 2, 
                            image=ImageTk.PhotoImage(image))



###################
#  Survival
###################

class Survival(object):
    
    groundBlock = 0

    @staticmethod
    def initialize(app):
        Survival.groundBlock = (app.loadImage('./assets/images/tiles.png')
                                        .crop((0, 0, 16, 16))
                                        .resize((32, 32)))
    
    def __init__(self):
        self.leftShift = 0

    def drawBlocks(self, app, canvas):
        cols = math.ceil(app.width / 32) + 1
        rows = 2

        for row in range(rows):
            for col in range(cols):
                cx = 32 * (col) + 16
                cy = app.height - row * 32 - 16
                canvas.create_image(cx, cy, 
                                image=ImageTk.PhotoImage(Survival.groundBlock))

    def redrawAll(self, app, canvas):
        canvas.create_rectangle(0, 0, app.width, app.height, fill="#5c94fc")
        self.drawBlocks(app, canvas)

def survival_redrawAll(app, canvas):
    app.survival.redrawAll(app, canvas)

def appStarted(app):

    app.map = Map(app, './assets/images/map1-1.png')

    Mario.initialize(app)
    app.mario = Mario(80, 385)

    app.timerDelay = 20

    app.block = (app.loadImage('./assets/images/tiles.png').crop((0, 0, 16, 16))
                                                           .resize((32, 32)))
    app.survival = Survival()
    app.survival.initialize(app)
    # app.mode = "survival"

    app._root.resizable(False, False)

def timerFired(app):
    if app.mario.xMotion != 0 or app.mario.xVelocity != 0:
        app.mario.move(app)

def keyPressed(app, event):

    print("key pressed")

    if event.key == 'Right':

        if app.mario.xMotion == -1: return

        app.mario.xMotion = 1

    elif event.key == 'Left':

        if app.mario.xMotion == 1: return

        app.mario.xMotion = -1
    elif event.key == 'Up':
        pass
        # app.mario.jump()

def keyReleased(app, event):

    print("key released")

    if event.key == 'Right' or event.key == 'Left':
        
        app.mario.xMotion = 0

def redrawAll(app, canvas):
    app.map.drawMap(app, canvas)
    app.mario.drawMario(app, canvas)

runApp(width=1280, height=480)