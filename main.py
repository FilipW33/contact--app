import tkinter as tk
from tkinter import ttk, messagebox
import com  #import library, where the application logic is

#database initialization
com.create_table()

#restart loads contacts already saved earlier
def refresh_contacts():
    for item in contact_list.get_children():
        contact_list.delete(item)
    for contact in com.get_contacts():
        contact_list.insert("", "end", values=contact)

# showing contacts and setting the main window
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
    tk.Button(form_window,text="Save",command=save).pack(pady=10)

#adding a new contact
def add_contact():
    def save_contact(data):
        try:
            com.add_contact(data["Name"],data["Surname"],data["Email"],data["Phone"])
            refresh_contacts()
            messagebox.showinfo("Sukces","Contact added successfully!")
        except ValueError as e:
            messagebox.showerror("Błąd",str(e))
    show_form("Add contact",["Name","Surname","Email","Phone"],on_save=save_contact)

#edition of contacts
def edit_contact():
    selected_item = contact_list.selection()
    if not selected_item:
        messagebox.showerror("Error”, ”No contact selected for editing.")
        return
    contact_id=contact_list.item(selected_item,"values")[0]
    current_values=contact_list.item(selected_item,"values")[1:]
    def update_contact(data):
        try:
            com.update_contact(contact_id,data["Name"],data["Surname"],data["Email"],data["Phone"])
            refresh_contacts()
            messagebox.showinfo("Contact updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error",str(e))
    show_form("Edit contact",["Name","Surname","Email","Phone"],defaults=current_values,on_save=update_contact)

#removal of contact
def delete_contact():
    selected_item = contact_list.selection()
    if selected_item:
        contact_id = contact_list.item(selected_item, "values")[0]
        com.delete_contact(contact_id)
        refresh_contacts()
        messagebox.showinfo("Success”, ”Contact removed successfully!")
    else:
        messagebox.showerror("Error”, ”No contact selected for deletion.")

#creating the main window
root = tk.Tk()
root.title("Contact management")
root.geometry("800x600")

#contact list
columns = ("ID","Name","Surname","Email","Phone")
contact_list = ttk.Treeview(root,columns=columns,show="headings")
#width of column ID
for col in columns:
    contact_list.heading(col,text=col)
contact_list.column("ID",width=10)
#width for other columns than ID
for col in columns[1:]:
    contact_list.column(col,width=150)
contact_list.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
#centering text
for col in columns:
    contact_list.heading(col,anchor="center")
    contact_list.column(col,anchor="center")

#buttons
btn_frame=tk.Frame(root)
btn_frame.pack(fill=tk.X)
buttons=[
    ("Add contact",add_contact),
    ("Edite contact",edit_contact),
    ("Delete contact",delete_contact),]
for text,command in buttons:
    tk.Button(btn_frame,text=text,command=command).pack(side=tk.LEFT,padx=5,pady=5)

#loading contacts
refresh_contacts()
root.mainloop()
