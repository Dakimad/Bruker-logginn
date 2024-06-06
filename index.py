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
SCREEN_WIDTH = 1200
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

def generate_unique_number():
    # Genererer et unikt 10-sifret tall
    while True:
        random_number = random.randint(1000000000, 9999999999)
        if not check_duplicate(random_number):
            return random_number

def check_duplicate(number):
    # Sjekker om tallet allerede eksisterer i databasen
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM Brukere WHERE BrukerID = %s", (number,))
        result = cursor.fetchone()
        return result['count'] > 0

def insert_user(username, bruker_id, passord):
    # Setter inn brukernavn, brukerID og passord i databasen
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO Brukere (Navn, BrukerID, Passord) VALUES (%s, %s, %s)", (username, bruker_id, passord))
    connection.commit()

def check_duplicate_user(username):
    # Sjekker om brukernavnet allerede eksisterer i databasen
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM Brukere WHERE Navn = %s", (username,))
        result = cursor.fetchone()
        return result['count'] > 0
