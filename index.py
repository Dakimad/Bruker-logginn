import pygame
import pymysql.cursors
import random
import re

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
        cursor.execute("SELECT COUNT(*) AS count FROM Brukere WHERE BrukerID = %s", (number))
        result = cursor.fetchone()
        if result['count'] > 0:
            return True
        else:
            return False

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
        if result['count'] > 0:
            return True
        else:
            return False

def insert_user(username, bruker_id, passord):
    # Setter inn brukernavn, brukerID og passord i databasen
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO Brukere (Navn, BrukerID, Passord) VALUES (%s, %s, %s)", (username, bruker_id, passord))
    connection.commit()

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

def main(): 
    # Sjekker om brukernavnet allerede er brukt
    while True:
        # Ber brukeren om å skrive inn et brukernavn
        print("Skriv inn et brukernavn:")
        username = input()
        
        # Sjekker om brukernavnet allerede er brukt
        if not check_duplicate_user(username):
            break
        print("Brukernavnet er allerede brukt. Velg et annet brukernavn.")
    
    while True:
        # Ber brukeren om å skrive inn et passord
        print("Skriv inn passord:")
        passord = input()
        
        # Sjekker om passordet er gyldig
        if is_valid_password(passord):
            break
        print("Passordet oppfyller ikke kravene. Det må være minst 8 tegn langt, inneholde minst en stor bokstav, et tall og et spesialtegn.")

    
    # Genererer et unikt brukerID
    bruker_id = generate_unique_number()
    
    # Setter inn brukernavn og brukerID i databasen
    insert_user(username, bruker_id, passord)

    # Skriver ut bekreftelse på at brukeren er lagt til i databasen
    print("Bruker lagt til i databasen med brukernavn:", username, ", BrukerID:", bruker_id, "og Passord", passord)

if __name__ == "__main__":
    main()
