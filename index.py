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

def main():
    font = pygame.font.Font(None, 32)
    input_box1 = pygame.Rect(300, 200, 140, 32)
    input_box2 = pygame.Rect(300, 250, 140, 32)
    register_button = pygame.Rect(300, 300, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive
    button_color = BLUE
    active1 = False
    active2 = False
    button_active = False
    text1 = ''
    text2 = ''
    error_message = ''
    success_message = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Sjekker om brukernavn tekstboksen er klikket på
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                    color1 = color_active if active1 else color_inactive
                else:
                    active1 = False
                    color1 = color_inactive
                # Sjekker om passord tekstboksen er klikket på
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                    color2 = color_active if active2 else color_inactive
                else:
                    active2 = False
                    color2 = color_inactive
                # Sjekker om registrer knappen er klikket på
                if register_button.collidepoint(event.pos):
                    button_active = True
                    # Validerer input og registrerer brukeren
                    if text1 and text2 and is_valid_password(text2):
                        if not check_duplicate_user(text1):
                            bruker_id = generate_unique_number()
                            insert_user(text1, bruker_id, text2)
                            print("Bruker lagt til i databasen med brukernavn:", text1, ", BrukerID:", bruker_id, "og Passord", text2)
                            success_message = f"Brukeren {text1} ble registrert med BrukerID: {bruker_id}"
                            text1 = ''
                            text2 = ''
                            active1 = False
                            active2 = False
                            error_message = ''
                        else:
                            error_message = "Dette brukernavnet er allerede brukt. Vennligst velg et nytt."
                            success_message = ''
                    else:
                        error_message = "Passordet må inneholde minst én stor bokstav, ett tall, ett spesialtegn og være minst 8 tegn langt."
                        success_message = ''
                    button_active = False
            if event.type == pygame.KEYDOWN:
                # Håndterer tekstinput i brukernavn og passord tekstboksene
                if active1:
                    if event.key == pygame.K_RETURN:
                        active1 = False
                        color1 = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        active2 = False
                        color2 = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        # Oppdaterer skjermen
        screen.fill((30, 30, 30))
        draw_text('Skriv inn brukernavn:', font, WHITE, screen, 60, 200)
        draw_text('Skriv inn passord:', font, WHITE, screen, 100, 250)
        txt_surface1 = font.render(text1, True, color1)
        txt_surface2 = font.render(text2, True, color2)
        width1 = max(200, txt_surface1.get_width()+10)
        input_box1.w = width1
        width2 = max(200, txt_surface2.get_width()+10)
        input_box2.w = width2
        screen.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
        screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)
        pygame.draw.rect(screen, LIGHT_BLUE if button_active else button_color, register_button)
        draw_text('Registrer', font, WHITE, screen, register_button.x+15, register_button.y+5)

        # Tegner feilmeldinger og suksessmeldinger
        if error_message:
            draw_error_message(error_message, font, RED, screen, 60, 350)
        
        if success_message:
            draw_success_message(success_message, font, GREEN, screen, 60, 350)

        pygame.display.flip()

if __name__ == "__main__":
    main()
