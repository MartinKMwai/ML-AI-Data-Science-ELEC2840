
from sense_hat import SenseHat
from random import randint
sense = SenseHat()

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
    
def random_colour():
  random_red = randint(0, 255)
  random_green = randint(0, 255)
  random_blue = randint(0, 255)
  return (random_red, random_green, random_blue)   



while True:
  sense.show_message("EEE is awesome!", text_colour=random_colour(), back_colour=random_colour(), scroll_speed=0.05)


