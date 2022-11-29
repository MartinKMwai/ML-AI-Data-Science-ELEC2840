from sense_hat import SenseHat
from time import sleep
from random import randint
import random
sense = SenseHat()

n = 3
m = 3

ball_position = [n, m] # coordinates of the starting position

def random_colour():
  random_red = randint(0, 255)
  random_green = randint(0, 255)
  random_blue = randint(0, 255)
  return (random_red, random_green, random_blue)

while True:
  sleep(1)	# sleep for 1 second

  r = randint(-1,1)
  s = randint(-1,1)
  
  #print(r)
  #print(s)
  while r==0 and s==0:
    r = randint(-1,1)
    s = randint(-1,1)
  else:
    x= n+r
    y= m+s
    if 0<x<8 and 0<y<8:
      ball_position[0] = x # generate a new x-position
      ball_position[1] = y # generate a new y-position
      n=x
      m=y
      
      sense.clear()
      sense.set_pixel(ball_position[0], ball_position[1], random_colour())
      
    if y>7 or y<0:
    
      y=1

      
    if x>7 or x<0:
      x=1



    ball_position[0] = x # generate a new x-position
    ball_position[1] = y # generate a new y-position
    n=x
    m=y
      
    sense.clear()
    sense.set_pixel(ball_position[0], ball_position[1], random_colour())
