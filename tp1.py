
from cmu_112_graphics import *

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

    def move(self, map, dx, dy):

        if dx > 0:

            if(self.spriteX < len(Mario.sprites) // 2 + 1):
                self.spriteX = len(Mario.sprites) // 2 + 1

            self.spriteX += 1
            if(self.spriteX >= len(Mario.sprites)):
                self.spriteX = len(Mario.sprites) // 2 + 1

            if(map.inMargin(self.left + Mario.width, dx)):
                map.scrollMap(dx)
            else:
                self.left += dx
            
            if self.left > Map.width - Mario.width:
                self.left = Map.width - Mario.width

        elif dx < 0:

            if(self.spriteX >= len(Mario.sprites) // 2 + 1):
                self.spriteX = len(Mario.sprites) // 2

            self.spriteX -= 1
            if(self.spriteX < 0):
                self.spriteX = len(Mario.sprites) // 2

            self.left += dx

            if self.left < 0:
                self.left = 0
    
    def drawMario(self, app, canvas):
        image = Mario.sprites[self.spriteX]
        canvas.create_image(self.left + Mario.width / 2, 
                            self.top + Mario.height / 2, 
                            image=ImageTk.PhotoImage(image))

def appStarted(app):
    Mario.initialize(app)
    app.mario = Mario(80, 385)
    app.map = Map(app, './assets/images/map1-1.png')

def keyPressed(app, event):
    if event.key == 'Right':
        app.mario.move(app.map, 20, 0)
    elif event.key == 'Left':
        app.mario.move(app.map, -20, 0)

def redrawAll(app, canvas):
    app.map.drawMap(app, canvas)
    app.mario.drawMario(app, canvas)

runApp(width=1280, height=480)