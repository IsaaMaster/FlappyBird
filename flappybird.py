from tkinter import Tk, Canvas
from random import randint
import time

def main():
    #main iteration
    while not gameOver:

        #update positions
        for obt in obts: obt.move()
        for cloud in clouds: cloud.move()
        
        fall(); day(); checkLoss() #game features
        
        window.update() #repacks the canvas
        time.sleep(gameStep) #waits for gameStep seconds

    #new highscore update,  w=write to file
    #file = open("highscore.txt", "w")
    #file.write(str(max(score, highScore))); file.close() #need to close file

    #end game stuff
    c.configure(bg=backgroundColor)
    c.create_text((canvasWidth/2, canvasHeight/2), text = "Game Over, your score is: " + str(score) , font=100) 
    window.update() 
    time.sleep(4)


window = Tk()
window.geometry("800x500") #WidthxHeight
window.configure(background = "black")
window.title("Flappy Dot Game")

#Game Configurations
canvasWidth = 800
canvasHeight = 500  
gravity = 3
ballSize = 20
flapHeight = 60
backgroundColor = "lightblue"
gameStep = 0.005

obstacleWidth = 50
gapHeight = 200
moveDist = 5  

#initially game not over
global gameOver
gameOver = False

#high score
score = 0

#highscore, r =read file
 

#create canvas
c = Canvas(window, bg=backgroundColor, height=canvasHeight, width=canvasWidth)

dirt = c.create_rectangle(0, canvasHeight-30, canvasWidth, canvasHeight, fill="chocolate4", outline="chocolate4")
grass = c.create_rectangle(0, canvasHeight-37, canvasWidth, canvasHeight-30, fill= "forestgreen", outline="forestgreen")

class Obstacle:
  def __init__(self, color, dist):
    #top rect top left point
    self.TopX0 = canvasWidth + dist*canvasWidth/3
    self.TopY0 = 0
    #top rect bottom right point
    self.TopX1 = canvasWidth + obstacleWidth +dist*canvasWidth/3
    self.TopY1 = randint(canvasHeight/10, canvasHeight - canvasHeight/10 - gapHeight)

    self.TopRect = c.create_rectangle(self.TopX0, self.TopY0, self.TopX1, self.TopY1, fill = color)

    #bottom rect top left point
    self.BotX0 = self.TopX0
    self.BotY0 = self.TopY1 + gapHeight
    #bottom rect bottom right point
    self.BotX1 = self.TopX1
    self.BotY1 = canvasHeight

    self.BotRect = c.create_rectangle(self.BotX0, self.BotY0, self.BotX1, self.BotY1, fill = color)

  def move(self):
    self.TopX0 -= moveDist; self.TopX1 -= moveDist #moving obsactles

    self.BotX0 -= moveDist; self.BotX1 -= moveDist
  
  

    if self.TopX1 <= 0: #reset if past left boundary
      self.TopX0 = canvasWidth
      self.TopY0 = 0
      self.TopX1 = canvasWidth + obstacleWidth
      self.TopY1 = randint(canvasHeight/10, canvasHeight - canvasHeight/10 - gapHeight)

      self.BotX0 = self.TopX0
      self.BotY0 = self.TopY1 + gapHeight
      self.BotX1 = self.TopX1
      self.BotY1 = canvasHeight
      global score
      score+=1
      
    c.coords(self.TopRect, self.TopX0, self.TopY0, self.TopX1, self.TopY1) #set coords
    c.coords(self.BotRect, self.BotX0, self.BotY0, self.BotX1, self.BotY1) #set coords

class cloud():
  def __init__(self):
    self.X0 = randint(canvasWidth, canvasWidth+200)
    self.Y0 = randint(0, int(canvasHeight/4))
    self.X1 = self.X0 + randint(200, 350)
    self.Y1= self.Y0 + 40
    self.rect = c.create_rectangle(self.X0, self.Y0, self.X1, self.Y1, fill = "white", outline = "white")
    self.speed = randint(2, 3)
  def move(self):
    self.X0 -=self.speed; self.X1 -=self.speed

    #reset if past boundary
    if self.X1 < 0:
      self.X0 = randint(canvasWidth, canvasWidth+200)
      self.Y0 = randint(0, int(canvasHeight/4))
      self.X1 = self.X0 + randint(200, 350)
      self.Y1= self.Y0 + 40
      self.speed = randint(2,3)
    c.coords(self.rect, self.X0, self.Y0, self.X1, self.Y1)

#list of clouds
clouds = [cloud() for i in range(5)]

#list of obstacles
obts = [Obstacle("light green", i+1) for i in range(3)]

#create dot
dot = c.create_oval(canvasWidth/6, canvasHeight/2, canvasWidth/6 + ballSize, canvasHeight/2 + ballSize, fill="yellow")


#put stuff on canvas
c.pack()

#'flap'
def flap(event):
  if not gameOver:
    dotCoords = c.coords(dot)#get coords
    c.coords(dot, dotCoords[0], dotCoords[1] - flapHeight, dotCoords[2], dotCoords[3] - flapHeight)#change coords

window.bind("<space>", flap)



#makes ball fall
def fall():
  dotCoords = c.coords(dot)#get coords
  c.coords(dot, dotCoords[0], dotCoords[1] + gravity, dotCoords[2], dotCoords[3] + gravity)#change coords

#checks if dot 'dies'
def checkLoss():
  global gameOver

  dotCoords = c.coords(dot) # dotCoords = [x0, y0, x1, y1]
  dotX = (dotCoords[0] + dotCoords[2]) / 2
  dotY = (dotCoords[1] + dotCoords[3]) / 2

  #gameover conditions
  if dotY >= canvasHeight or dotY <= 0:
    gameOver = True

  for obt in obts:
  #Checking to see if part of the ball in within the x coords of the obstacle and above or below the gap 
    if  dotCoords[2] > obt.TopX0 and dotCoords[0] < obt.TopX1 and (dotCoords[1] < obt.TopY1 or dotCoords[3] > obt.BotY0):
        gameOver = True

#changes to night after certain time
def day():
  global c
  if (score//25)%2==1: #changes every 25 scores
    c.configure(bg="blue4") #night color
  else:
    c.configure(bg=backgroundColor)


    

main()