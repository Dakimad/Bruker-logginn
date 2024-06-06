import pygame
import pymysql.cursors
import random
import re

# Farger
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Skjermstørrelse
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialiserer Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brukerregistrering")

# Oppretter en tilkobling til databasen
connection = pymysql.connect(host='172.20.128.73',
                             user='Daniel',
                             password='123Akademiet',
                             database='Users',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)