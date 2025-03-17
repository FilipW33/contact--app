import sqlite3
import re


#database creation
connection=sqlite3.connect('kontakty.db')

#creation of records in database, in case of phone and email will return error in case of duplication
def create_table():
    with connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS kontakty(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE)""")
        
#function of adding a contact, with checking emails and phone
def add_contact(name,surname,email,phone):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Incorrect email format!")
    if not re.match(r"^\+?\d{7,15}$",phone):
        raise ValueError("Incorrect phone number format!")
    with connection:
        connection.execute("""INSERT INTO kontakty(name,surname,email,phone)VALUES(?,?,?,?)""",
                           (name,surname,email,phone))
#showing contacts
def get_contacts():    
    with connection:
        return connection.execute("""SELECT * FROM kontakty""").fetchall() #fetchall retrieves all query results alternative fetchmany(e.g.5) will return only 5 rows
    
#remove contact by id number (safest because id is unique)
#the only downside if we remove id=2 and add another contact it will have id number 3 not 2
def delete_contact(contact_id):
    with connection:
        connection.execute("""DELETE FROM kontakty WHERE id = ?""",(contact_id,))

#update contact function
def update_contact(contact_id,name=None,surname=None,email=None,phone=None):
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Incorrect email format!")
    if phone and not re.match(r"^\+?\d{7,15}$", phone):
        raise ValueError("Incorrect phone number format!")
    with connection:
        contact=connection.execute("""SELECT * FROM kontakty WHERE id = ?""",(contact_id,)).fetchone()
        if not contact:
            raise ValueError("The contact with the specified ID does not exist.")
        #the ability for the user to change only the data they want and not all of it 
        name=name or contact[1]
        surname=surname or contact[2]
        email=email or contact[3]
        phone=phone or contact[4]
        connection.execute("""UPDATE kontakty
            SET name = ?, surname = ?, email = ?, phone = ?
            WHERE id = ?""",(name,surname,email,phone,contact_id))
