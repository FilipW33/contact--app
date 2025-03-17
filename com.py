import sqlite3
import re

#tworzenie bazy danych
connection=sqlite3.connect('kontakty.db')
#tworzenie rekordów w bazie danych, w przypadku telefonu i maila zwróci błąd w  przypadku duplikacji
def create_table():
    with connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS kontakty(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE)""")
#funkcja dodania kontaktu, ze sprawdzaniem maili i telefonu
def add_contact(name,surname,email,phone):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Nieprawidłowy format email!")
    if not re.match(r"^\+?\d{7,15}$",phone):
        raise ValueError("Nieprawidłowy format numeru telefonu!")
    with connection:
        connection.execute("""INSERT INTO kontakty(name,surname,email,phone)VALUES(?,?,?,?)""",
                           (name,surname,email,phone))
#wyświetlanie kontaktów
def get_contacts():    
    with connection:
        return connection.execute("""SELECT * FROM kontakty""").fetchall() #fetchall pobiera wszystkie wyniki zapytania alternatywa fetchmany(np.5) zwróci tylko 5 wierszy
    
#usuwanie kontaku po numerze id (najbezpieczniej gdyż id jest unikalny)
#jedyny minus jak usuniemy id=2 i dodamy kolejny kontakt to będzie miał id numer 3 a nie 2
def delete_contact(contact_id):
    with connection:
        connection.execute("""DELETE FROM kontakty WHERE id = ?""",(contact_id,))

#funckja updatu kontaktu
def update_contact(contact_id,name=None,surname=None,email=None,phone=None):
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Nieprawidłowy format email!")
    if phone and not re.match(r"^\+?\d{7,15}$", phone):
        raise ValueError("Nieprawidłowy format numeru telefonu!")
    with connection:
        contact=connection.execute("""SELECT * FROM kontakty WHERE id = ?""",(contact_id,)).fetchone()
        if not contact:
            raise ValueError("Kontakt o podanym ID nie istnieje.")
        #możliwość zmiany przez użytkownika tylko tych danych które chce a nie wszystkich 
        name=name or contact[1]
        surname=surname or contact[2]
        email=email or contact[3]
        phone=phone or contact[4]
        connection.execute("""UPDATE kontakty
            SET name = ?, surname = ?, email = ?, phone = ?
            WHERE id = ?""",(name,surname,email,phone,contact_id))
