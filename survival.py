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

    width = 28
    height = 25
    
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
            sprite = sprite.resize((Mario.width, Mario.height))
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

        self.level = 0

    # Moves mario to the right by xVelocity amount
    def moveRight(self, app):

        # collided = app.map.collided(self.top, self.left + Mario.width,
        #                     self.top + Mario.height, self.left,
        #                     self.xVelocity, self.yVelocity)

        # if collided[0] and collided[1] == "left":
        #     self.xVelocity = 0
        #     self.left = collided[2] - Mario.width
        #     return

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

        # collided = app.map.collided(self.top, self.left + Mario.width,
        #                     self.top + Mario.height, self.left,
        #                     self.xVelocity, self.yVelocity)

        # if collided[0] and collided[1] == "right":
        #     self.xVelocity = 0
        #     self.left = collided[2]
        #     return

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
            # Accelerates by 1.3 times until reaches 10
            elif self.xVelocity < 10:
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
            # Accelerates by 1.3 times until reaches -10
            elif self.xVelocity > -10:
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

    def fall(self, map):

        if self.yMotion == 1: return

        collided = map.collided(self.top, self.left + Mario.width,
                            self.top + Mario.height, self.left,
                            0, 5)

        if not collided[0] and self.top < map.height - 89:
            if self.yVelocity == 0:
                self.yMotion = 0
                self.yVelocity = 5

    # Does one small part of jumping at a time
    def jump(self, map):

        # Sets initial yVelocity to 35 if mario were static
        if self.yVelocity == 0:

            self.yVelocity = 20

        # If character is falling below the leveled ground then set
        # character to be on the ground
        if (self.yMotion == 0 
            and self.top + self.yVelocity > map.level0 - Mario.height):

            self.top = map.level0 - Mario.height
            self.yVelocity = 0

        # If character is falling, increase top margin by yVelocity
        # Then increase falling speed by 1.25 times
        elif self.yMotion == 0:

            self.top += self.yVelocity
            if self.yVelocity < 30:
                self.yVelocity *= 1.25
        
        # If character is jumping, decrease top margin by yVelocity
        # Then decrease speed going up by 1.3 times
        else:

            self.top -= self.yVelocity
            self.yVelocity /= 1.2
        
        # If yVelocity is near 0, set it to 0
        if self.yVelocity < 3:

            self.yMotion = 0
        
        collided = map.collided(self.top, self.left + Mario.width,
                            self.top + Mario.height, self.left,
                            self.xVelocity, self.yVelocity)

        if collided[0]:

            if collided[1] == "top":
                
                self.yMotion = 0

            elif collided[1] == "bottom":

                self.yVelocity = 0
                self.yMotion = 0
                self.level = 1

                self.top = collided[2] - Mario.height

            return
    
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
    def __init__(self, app, blockWidth):

        self.app = app

        # For scrolling effect
        self.leftShift = 0

        # images from http://www.mariouniverse.com/sprites-nes-smb/
        self.groundBlock = (app.loadImage('./assets/images/tiles.png')
                                        .crop((0, 0, 16, 16))
                                        .resize((blockWidth, blockWidth)))
        
        # Width of ground block
        self.blockWidth = blockWidth
    
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


class Blocks(object):

    def __init__(self, app, blockWidth, mapWidth):

        self.app = app
        self.blockWidth = blockWidth

        self.maxBlocks = mapWidth // blockWidth

        self.blocks = []

        for i in range(6, 10):
            self.blocks.append(Block(app, blockWidth, 1, blockWidth * i, 5, i - 4))

        self.startPos = Block(app, blockWidth, 1, blockWidth * 5, 5, 0)

        self.blocks.append(self.startPos)

        for i in range(0, 5):
            self.blocks.append(Block(app, blockWidth, 2, mapWidth - blockWidth * i, 5, 4 - i))

        self.finalBlock = Block(app, blockWidth, 2, mapWidth - blockWidth * 5, 5, 0)
        
        self.blocks.append(self.finalBlock)

        while not self.completeLevel():
            pass

        for block in self.blocks:
            if block == self.startPos or block == self.finalBlock: continue
            block.addGoomba()
    

    def getNewBlock(self, blocksTried, length):

        level = random.randint(1, 4)
        leftPosition = random.randint(0, self.maxBlocks)

        thisBlock = Block(self.app, self.blockWidth, level, self.blockWidth * leftPosition, length, 0)

        for block in self.blocks:

            if block.left == thisBlock.left:

                return self.getNewBlock(blocksTried, length)
        
        for block in blocksTried:

            if block == thisBlock:

                return self.getNewBlock(blocksTried, length)
        
        return thisBlock
    
    def blockConnected(self, fromBlock, toBlock):

        return (abs(fromBlock.left - toBlock.left) // self.blockWidth < 6
                and (toBlock.level <= fromBlock.level + 1))

    def blockIsReachebleHelper(self, startBlock, endBlock):

        visited = []

        val = self.blockIsReachable(startBlock, endBlock, visited)

        return val

    def blockIsReachable(self, currBlock, finalBlock, visited):

        for block in visited:

            if currBlock == block:

                return False
        
        visited.append(currBlock)

        if currBlock == finalBlock or self.blockConnected(currBlock, finalBlock): return True

        for block in self.blocks:

            if block == currBlock or block == finalBlock: continue

            if (self.blockConnected(currBlock, block) 
                    and self.blockIsReachable(block, finalBlock, visited)):
                
                return True
        
        return False

    def numOfBlocks(self):

        rand = random.random()

        if rand < 0.2:
            return 1
        elif rand < 0.5:
            return 2
        elif rand < 0.8:
            return 3
        else:
            return 4

    def completeLevel(self):

        blocksTried = []

        while len(blocksTried) < 10:

            numOfBlocks = self.numOfBlocks()
            newBlock = self.getNewBlock(blocksTried, numOfBlocks)

            newBlocks = [newBlock]

            for i in range(numOfBlocks):
                newBlocks.append(Block(self.app, self.blockWidth, newBlock.level, newBlock.left + self.blockWidth * (i + 1), numOfBlocks, i + 1))

            self.blocks = self.blocks + newBlocks

            if self.blockIsReachebleHelper(self.startPos, newBlock):

                if self.blockIsReachebleHelper(self.startPos, self.finalBlock):

                    return True
                
                else:

                    if self.completeLevel():

                        return True
        
            blocksTried.append(newBlock)

            for block in newBlocks:
                self.blocks.remove(block)
        
        return False


    
    def scrollBlocks(self, xVelocity):

        for block in self.blocks:
            block.scrollBlock(xVelocity)
    
    def drawBlocks(self, canvas):

        for block in self.blocks:
            block.drawBlock(canvas)
    
    def collided(self, top, right, bottom, left, xVelocity, yVelocity):
        
        for block in self.blocks:
            collision = block.collided(top, right, bottom, left, xVelocity, yVelocity)
            if collision[0]:
                return collision
        
        return (False, None, None)


class Block(object):

    block = None
    blockWidth = 0

    def __init__(self, app, blockWidth, level, left, length, index):

        if Block.block == None:
            Block.block = (app.loadImage('./assets/images/tiles.png')
                                        .crop((16, 0, 32, 16))
                                        .resize((blockWidth, blockWidth)))
        if Block.blockWidth == 0:
            Block.blockWidth = blockWidth
        
        self.level = level
        self.top = app.height - blockWidth * 2 - blockWidth * 3 * level
        self.left = left

        self.index = index
        self.length = length

        self.goomba = None

        self.app = app
    
    def addGoomba(self):

        if self.length >= 3 and self.index == 0 and random.random() <= 0.7:
            self.goomba = Goomba(self.top - Goomba.height, self.left)
            self.app.goombas.append(self.goomba)
    
    def collided(self, top, right, bottom, left, xVelocity, yVelocity):

        if xVelocity != 0 and (top > self.top - Block.blockWidth and bottom < self.top):

            if right < self.left + Block.blockWidth and right - xVelocity > self.left:
                return (True, "right", self.left)
            elif left > self.left and left - xVelocity < self.left + Block.blockWidth:
                return (True, "left", self.left + Block.blockWidth)
        
        if yVelocity != 0 and (right > self.left and left < self.left + Block.blockWidth):

            if top > self.top and top - yVelocity < self.top + Block.blockWidth:
                return (True, "top", self.top + Block.blockWidth)
            elif bottom < self.top + Block.blockWidth and bottom + yVelocity > self.top:
                return (True, "bottom", self.top)
        
        return (False, 0, 0)
    
    def __eq__(self, other):

        return (isinstance(other, Block) and self.level == other.level
                and self.left == other.left)
    
    def scrollBlock(self, xVelocity):

        self.left -= xVelocity
    
    def drawBlock(self, canvas):

        if self.left > self.app.width + self.app.map.leftShift: return

        cx = self.left + Block.blockWidth / 2
        cy = self.top + Block.blockWidth / 2

        canvas.create_image(cx, cy, 
                                image=ImageTk.PhotoImage(Block.block))
        canvas.create_text(cx, cy, text=f"{self.index}", fill="white")



class Goomba(object):

    sprites = []
    width = 32
    height = 32

    def initialize(app):

        sprite1 = (app.loadImage('./assets/images/enemies.png')
                                        .crop((0, 4, 16, 20))
                                        .resize((Goomba.width, Goomba.height)))
        sprite2 = (app.loadImage('./assets/images/enemies.png')
                                        .crop((20, 4, 36, 20))
                                        .resize((Goomba.width, Goomba.height)))
        Goomba.sprites.append(sprite1)
        Goomba.sprites.append(sprite2)
    
    def __init__(self, top, left):
        self.top = top
        self.left = left
        self.sprite = 0

    def scrollGoomba(self, xVelocity):
        self.left -= xVelocity
    
    def drawGoomba(self, canvas):

        cx = self.left + Goomba.width / 2
        cy = self.top + Goomba.height / 2

        canvas.create_image(cx, cy, 
                                image=ImageTk.PhotoImage(Goomba.sprites[self.sprite]))


###################
#  Survival Map
###################

class Survival(object):
    
    # constructor
    def __init__(self, app):

        self.app = app

        self.leftShift = 0

        self.maxWidth = 3584
        self.height = app.height
        
        # Sets left and right margin for when map scrolls
        self.margin = 250

        # Sets width and height of blocks to be 32
        self.blockDimension = 32

        # Sets up the ground blocks
        self.groundBlocks = GroundBlocks(app, self.blockDimension)

        # Ground height
        self.level0 = app.height - self.blockDimension * 2

        # Sets up the clouds
        self.clouds = Clouds(app)
        
        # Sets up the blocks
        self.blocks = Blocks(app, self.blockDimension, self.maxWidth)

    # Checks if character is going to be in the right margin of map
    def inRightMargin(self, right, xVelocity):
        return self.leftShift + self.app.width < self.maxWidth and right + xVelocity > self.app.width - self.margin

    # Checks if character is going to be in the left margin of map
    def inLeftMargin(self, left, xVelocity):
        return self.leftShift > 0 and left + xVelocity < self.margin
    

    def collided(self, top, right, bottom, left, xVelocity, yVelocity):

        return self.blocks.collided(top, right, bottom, left, xVelocity, yVelocity)

    # Scrolls the map by xVelocity
    def scrollMap(self, xVelocity):

        self.leftShift += xVelocity

        # Scrolls the ground blocks
        self.groundBlocks.scrollBlocks(xVelocity)

        # Scrolls the blocks
        self.blocks.scrollBlocks(xVelocity)

        # Moves the clouds
        self.clouds.moveClouds(xVelocity)

        for goomba in self.app.goombas:
            goomba.scrollGoomba(xVelocity)
    

    # Draw background and everything in map
    def drawMap(self, canvas):
        canvas.create_rectangle(0, 0, self.app.width, self.app.height, 
                                fill="#5c94fc")
        self.clouds.drawClouds(canvas)
        self.groundBlocks.drawBlocks(canvas)
        self.blocks.drawBlocks(canvas)

# Draws everything in survival mode
def survival_redrawAll(app, canvas):
    app.map.drawMap(canvas)
    app.mario.drawMario(canvas)
    for goomba in app.goombas:
        goomba.drawGoomba(canvas)

# Controller
def survival_timerFired(app):

    # Moves if mario should be moving
    if app.mario.xMotion != 0 or app.mario.xVelocity != 0:
        app.mario.move(app)
    
    # Jump if mario should be jumping
    if app.mario.yMotion != 0 or app.mario.yVelocity != 0:
        app.mario.jump(app.map)
    
    app.mario.fall(app.map)

# Controller
def survival_keyPressed(app, event):

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

    if event.key == 'Right' or event.key == 'Left':
        
        app.mario.xMotion = 0

# Model
def appStarted(app):

    # Starts off in title screen
    app.mode = "titleScreen"
    app.timerDelay = 20

    app.goombas = []

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
        app.mario = Mario(160, app.height - 188)
        app.mario.jump(app.map)

        Goomba.initialize(app)
        # app.goombas.append(Goomba(200, 400))

runApp(width=1280, height=480)