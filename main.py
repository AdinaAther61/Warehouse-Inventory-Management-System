"""
Warehouse Inventory System - GUI Version
==========================================


way: python warehouse_gui.py
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox


# ------------------------------------------------------------------
# DATA LAYER - same logic which is implement in console version
# ------------------------------------------------------------------

def load_data():
    """Load data from file. In first attemp an epty dictionary."""
    try:
        file = open("warehouse.json", "r")
        data = json.load(file)
        file.close()
    except:
        data = {}
    return data


def save_data(data):
    """Sve warehouse dictionary in file."""
    file = open("warehouse.json", "w")
    json.dump(data, file)
    file.close()


# before startingg program load previous data
warehouse = load_data()


# ------------------------------------------------------------------
# GUI SETUP
# ------------------------------------------------------------------

root = tk.Tk()
root.title("Warehouse Inventory System")
root.geometry("800x550")
root.configure(bg="#f4f6f8")

# ---- Style for the table (Treeview) ----
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

# ---- Title label at the top ----
title_label = tk.Label(
    root, text="Warehouse Inventory System",
    font=("Segoe UI", 18, "bold"), bg="#f4f6f8", fg="#1f2937", pady=15
)
title_label.pack()


# ------------------------------------------------------------------
# FORM SECTION (Name, Quantity, Price, Category inputs)
# ------------------------------------------------------------------

form_frame = tk.Frame(root, bg="#f4f6f8")
form_frame.pack(pady=10)

# For every fieldLabel + Entry (text box) 

tk.Label(form_frame, text="Item Name", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=0, column=0, padx=8, pady=5)
name_entry = tk.Entry(form_frame, width=15)
name_entry.grid(row=1, column=0, padx=8)

tk.Label(form_frame, text="Quantity", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=0, column=1, padx=8, pady=5)
quantity_entry = tk.Entry(form_frame, width=15)
quantity_entry.grid(row=1, column=1, padx=8)

tk.Label(form_frame, text="Price", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=0, column=2, padx=8, pady=5)
price_entry = tk.Entry(form_frame, width=15)
price_entry.grid(row=1, column=2, padx=8)

tk.Label(form_frame, text="Category", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=0, column=3, padx=8, pady=5)
category_entry = tk.Entry(form_frame, width=15)
category_entry.grid(row=1, column=3, padx=8)


def clear_form():
    """All text boxes are empty."""
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)


def refresh_table():
    """Table :again fill with waehouse dictionary."""
    # 
    for row in tree.get_children():
        tree.delete(row)
    # 
    for name in warehouse:
        item = warehouse[name]
        tree.insert("", tk.END, values=(name, item["quantity"], item["price"], item["category"]))


# ------------------------------------------------------------------
# BUTTON ACTIONS (add / update / delete / search / clear)
# ------------------------------------------------------------------

def add_item():
    name = name_entry.get().strip()

    if name == "":
        messagebox.showwarning("Missing info", "Item ka naam likhein")
        return

    try:
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
    except:
        messagebox.showerror("Invalid input", "Quantity aur Price number honi chahiye")
        return

    category = category_entry.get().strip()

    warehouse[name] = {"quantity": quantity, "price": price, "category": category}
    save_data(warehouse)
    refresh_table()
    clear_form()


def delete_item():
    selected = tree.selection()   # user ne table mein jo row select ki hai

    if not selected:
        messagebox.showwarning("No selection", "Pehle table se koi item select karein")
        return

    # Selected row se item ka naam nikalte hain
    values = tree.item(selected[0], "values")
    name = values[0]

    if name in warehouse:
        del warehouse[name]
        save_data(warehouse)
        refresh_table()


def update_item():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("No selection", "Pehle table se koi item select karein")
        return

    values = tree.item(selected[0], "values")
    old_name = values[0]

    name = name_entry.get().strip()
    if name == "":
        name = old_name   

    try:
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
    except:
        messagebox.showerror("Invalid input", "Quantity aur Price number honi chahiye")
        return

    category = category_entry.get().strip()

    # (updated) 
    del warehouse[old_name]
    warehouse[name] = {"quantity": quantity, "price": price, "category": category}

    save_data(warehouse)
    refresh_table()
    clear_form()


def search_item():
    query = name_entry.get().strip().lower()

    for row in tree.get_children():
        tree.delete(row)

    for name in warehouse:
        if query in name.lower():   # partial match 
            item = warehouse[name]
            tree.insert("", tk.END, values=(name, item["quantity"], item["price"], item["category"]))


def on_row_select(event):
    
    selected = tree.selection()
    if not selected:
        return
    values = tree.item(selected[0], "values")
    clear_form()
    name_entry.insert(0, values[0])
    quantity_entry.insert(0, values[1])
    price_entry.insert(0, values[2])
    category_entry.insert(0, values[3])


# ------------------------------------------------------------------
# BUTTONS
# ------------------------------------------------------------------

button_frame = tk.Frame(root, bg="#f4f6f8")
button_frame.pack(pady=10)

btn_style = {"font": ("Segoe UI", 10, "bold"), "width": 12, "pady": 5, "bd": 0}

tk.Button(button_frame, text="Add", bg="#2563eb", fg="white", command=add_item, **btn_style).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update", bg="#16a34a", fg="white", command=update_item, **btn_style).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete", bg="#dc2626", fg="white", command=delete_item, **btn_style).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Search", bg="#7c3aed", fg="white", command=search_item, **btn_style).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Show All", bg="#64748b", fg="white", command=refresh_table, **btn_style).grid(row=0, column=4, padx=5)
tk.Button(button_frame, text="Clear Form", bg="#94a3b8", fg="white", command=clear_form, **btn_style).grid(row=0, column=5, padx=5)


# ------------------------------------------------------------------
# TABLE (Treeview) - show all items in excel like table
# ------------------------------------------------------------------

table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="both", expand=True, padx=20)

columns = ("Name", "Quantity", "Price", "Category")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_row_select)   # 

# fill table with previous data
refresh_table()

root.mainloop()