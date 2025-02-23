import tkinter as tk
from tkinter import simpledialog, messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="library"
)

mycursor = mydb.cursor()

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    copies_available = int(copies_entry.get())

    if title == '' or author == '':
        messagebox.showerror('Error', 'Please fill all required fields')
        return

    sql = "INSERT INTO books (title, author, copies_available, copies_sold) VALUES (%s, %s, %s, 0)"
    val = (title, author, copies_available)
    mycursor.execute(sql, val)
    mydb.commit()
    messagebox.showinfo('Success', 'Book added successfully')
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    copies_entry.delete(0, 'end')

def delete_book():
    book_id = simpledialog.askinteger("Delete Book", "Enter book ID to delete:")
    if book_id is not None:
        sql = "DELETE FROM books WHERE id = %s"
        val = (book_id,)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo('Success', 'Book deleted successfully')

def sell_book():
    book_id = simpledialog.askinteger("Sell Book", "Enter book ID to sell:")
    if book_id is not None:
        copies_sold = simpledialog.askinteger("Sell Book", "Enter number of copies sold:")
        if copies_sold is not None:
            sql_select = "SELECT copies_available, copies_sold FROM books WHERE id = %s"
            val_select = (book_id,)
            mycursor.execute(sql_select, val_select)
            result = mycursor.fetchone()
            if result:
                available = result[0]
                sold = result[1]
                if copies_sold <= available:
                    new_available = available - copies_sold
                    new_sold = sold + copies_sold
                    sql_update = "UPDATE books SET copies_available = %s, copies_sold = %s WHERE id = %s"
                    val_update = (new_available, new_sold, book_id)
                    mycursor.execute(sql_update, val_update)
                    mydb.commit()
                    messagebox.showinfo('Success', 'Book sold successfully')
                else:
                    messagebox.showerror('Error', 'Not enough copies available')
            else:
                messagebox.showerror('Error', 'Book not found')

def view_books():
    mycursor.execute("SELECT * FROM books")
    books = mycursor.fetchall()
    books_listbox.delete(0, 'end')
    for book in books:
        books_listbox.insert('end', f"{book[0]} - {book[1]} by {book[2]} - Copies: {book[3]}")

def view_book_details():
    book_id = simpledialog.askinteger("View Book Details", "Enter book ID:")
    if book_id is not None:
        sql = "SELECT * FROM books WHERE id = %s"
        val = (book_id,)
        mycursor.execute(sql, val)
        book = mycursor.fetchone()
        if book:
            messagebox.showinfo('Book Details', f"Title: {book[1]}\nAuthor: {book[2]}\nCopies Available: {book[3]}\nCopies Sold: {book[4]}")
        else:
            messagebox.showinfo('Info', 'Book not found')

root = tk.Tk()
root.title("Library Management System")
root.resizable(False, False)  # إلغاء زر التكبير وتعطيل تغيير حجم النافذة

title_label = tk.Label(root, text="Title:")
title_label.grid(row=0, column=0, padx=10, pady=5)
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=0, column=1, padx=10, pady=5)

author_label = tk.Label(root, text="Author:")
author_label.grid(row=1, column=0, padx=10, pady=5)
author_entry = tk.Entry(root, width=50)
author_entry.grid(row=1, column=1, padx=10, pady=5)

copies_label = tk.Label(root, text="Copies Available:")
copies_label.grid(row=2, column=0, padx=10, pady=5)
copies_entry = tk.Entry(root, width=50)
copies_entry.grid(row=2, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Book", command=add_book, width=20)
add_button.grid(row=3, column=0, padx=10, pady=5)

delete_button = tk.Button(root, text="Delete Book", command=delete_book, width=20)
delete_button.grid(row=3, column=1, padx=10, pady=5)

sell_button = tk.Button(root, text="Sell Book", command=sell_book, width=20)
sell_button.grid(row=4, column=0, padx=10, pady=5)

view_button = tk.Button(root, text="View All Books", command=view_books, width=20)
view_button.grid(row=4, column=1, padx=10, pady=5)

details_button = tk.Button(root, text="View Book Details", command=view_book_details, width=20)
details_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

books_listbox = tk.Listbox(root, width=100)
books_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
