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

def is_valid_password(password):
    # Sjekker om passordet oppfyller kravene
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def draw_text(text, font, color, surface, x, y):
    # Tegner tekst på skjermen
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_error_message(message, font, color, surface, x, y):
    # Tegner feilmelding på skjermen
    error_text = font.render(message, True, color)
    surface.blit(error_text, (x, y))

def draw_success_message(message, font, color, surface, x, y):
    # Tegner suksessmelding på skjermen
    success_text = font.render(message, True, color)
    surface.blit(success_text, (x, y))

