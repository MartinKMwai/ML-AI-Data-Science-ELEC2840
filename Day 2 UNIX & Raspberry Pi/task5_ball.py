from time import sleep
from sense_hat import SenseHat
from random import randint
sense = SenseHat()

ball_position = [3, 3]
ball_velocity = [1, 1]
bat_pos = 4
b=5
m=3

def random_colour():
  random_red = randint(0, 255)
  random_green = randint(0, 255)
  random_blue = randint(0, 255)
  return (random_red, random_green, random_blue)
  
def draw_bat():
  global m
  for n in range(-1,m):
      sense.set_pixel(0, bat_pos+n, random_colour())


def move_up(event):
  global bat_pos
  if bat_pos > 1 and event.action=='pressed':
    bat_pos -= 1
    
def move_down(event):  
  global bat_pos
  global b
  if bat_pos < b and event.action=='pressed':
    bat_pos += 1
    
def draw_ball():
  global ball_position
  # Draws the ball pixel
  sense.set_pixel(ball_position[0], ball_position[1], 255, 255, 255)
  # Moves the ball to the next position
  ball_position[0] += ball_velocity[0]
  ball_position[1] += ball_velocity[1]



    
  if ball_position[1] == 0 or ball_position[1] == 7:
    ball_velocity[1] = -ball_velocity[1]
    
    global m
    
  if ball_position[0] == 7:
    ball_velocity[0] = -ball_velocity[0]    
    
    
  elif  ball_position[0] == 0 :
    ball_velocity[0] = -ball_velocity[0]
    
    global b
    m= m-1
    b= b+1
    if m == -1:
      sense.show_message("GAME OVER", text_colour=random_colour(), back_colour=random_colour(), scroll_speed=0.2)
    
  if ball_position[0] == 1 and bat_pos-m+1 <= ball_position[1] <= bat_pos+m:
    ball_velocity[0] = -ball_velocity[0]

            
sense.stick.direction_up = move_up
sense.stick.direction_down = move_down


while True:
  sense.clear(0, 0, 0)
  draw_bat()
  draw_ball()
  sleep(0.25)


    
