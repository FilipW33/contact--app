import tkinter as tk
from tkinter import ttk, messagebox
import com  #import biblioteki, gdzie jest logika aplikacji

#inicjalizacja bazy danych
com.create_table()

#podczas ponownego uruchomienia wczytuje kontakty już zapisane wcześniej
def refresh_contacts():
    for item in contact_list.get_children():
        contact_list.delete(item)
    for contact in com.get_contacts():
        contact_list.insert("", "end", values=contact)
# pokazywanie kontaktów i ustawienie głównego okna
def show_form(title, fields, defaults=None, on_save=None):
    form_window = tk.Toplevel(root)
    form_window.title(title)
    form_window.geometry("400x300")

    entries = {}
    for i,field in enumerate(fields):
        tk.Label(form_window,text=field+":").pack(pady=5)
        entry=tk.Entry(form_window)
        entry.pack(pady=5,padx=10,fill=tk.X)
        if defaults and i<len(defaults):
            entry.insert(0,defaults[i])
        entries[field]=entry

    def save():
        if on_save:
            data={field: entry.get() for field,entry in entries.items()}
            on_save(data)
        form_window.destroy()
    tk.Button(form_window,text="Zapisz",command=save).pack(pady=10)

#dodanie nowego kontaktu
def add_contact():
    def save_contact(data):
        try:
            com.add_contact(data["Imię"],data["Nazwisko"],data["Email"],data["Telefon"])
            refresh_contacts()
            messagebox.showinfo("Sukces","Kontakt dodany pomyślnie!")
        except ValueError as e:
            messagebox.showerror("Błąd",str(e))
    show_form("Dodaj kontakt",["Imię","Nazwisko","Email","Telefon"],on_save=save_contact)

#edycja kontaktów
def edit_contact():
    selected_item = contact_list.selection()
    if not selected_item:
        messagebox.showerror("Błąd","Nie wybrano kontaktu do edycji.")
        return
    contact_id=contact_list.item(selected_item,"values")[0]
    current_values=contact_list.item(selected_item,"values")[1:]
    def update_contact(data):
        try:
            com.update_contact(contact_id,data["Imię"],data["Nazwisko"],data["Email"],data["Telefon"])
            refresh_contacts()
            messagebox.showinfo("Kontakt zaktualizowany pomyślnie!")
        except ValueError as e:
            messagebox.showerror("Błąd",str(e))
    show_form("Edytuj kontakt",["Imię","Nazwisko","Email","Telefon"],defaults=current_values,on_save=update_contact)

#usuwanie kontaktu
def delete_contact():
    selected_item = contact_list.selection()
    if selected_item:
        contact_id = contact_list.item(selected_item, "values")[0]
        com.delete_contact(contact_id)
        refresh_contacts()
        messagebox.showinfo("Sukces", "Kontakt usunięty pomyślnie!")
    else:
        messagebox.showerror("Błąd", "Nie wybrano kontaktu do usunięcia.")

#tworzenie głównego okna
root = tk.Tk()
root.title("Zarządzanie kontaktami")
root.geometry("800x600")

#lista kontaktów

columns = ("ID","Imię","Nazwisko","Email","Telefon")
contact_list = ttk.Treeview(root,columns=columns,show="headings")
#szerokość kolumny ID
for col in columns:
    contact_list.heading(col,text=col)
contact_list.column("ID",width=10)
#szerokość kolmun prócz ID
for col in columns[1:]:
    contact_list.column(col,width=150)
contact_list.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
#centrowanie tekstu
for col in columns:
    contact_list.heading(col,anchor="center")
    contact_list.column(col,anchor="center")

#przyciski
btn_frame=tk.Frame(root)
btn_frame.pack(fill=tk.X)
buttons=[
    ("Dodaj kontakt",add_contact),
    ("Edytuj kontakt",edit_contact),
    ("Usuń kontakt",delete_contact),]
for text,command in buttons:
    tk.Button(btn_frame,text=text,command=command).pack(side=tk.LEFT,padx=5,pady=5)

#wczytywanie kontaktów
refresh_contacts()
root.mainloop()
