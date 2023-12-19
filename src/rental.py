import tkinter as tk
import sqlite3
import random
from tkinter import ttk
from datetime import datetime

class RentalSystem:

    def rental_book1(self):
        id = self.entry_rental_book_id.get()
        print('id', id)
        quantity = self.entry_rental_quantity1.get()
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book = self.cursor.fetchone()
        print(book)
        if int(book[3]) - int(quantity) < 0:
            self.label_rental_quantity3 = tk.Label(self.tab_rental, text='书籍数量不足,已全部租借')
            self.label_rental_quantity3.grid(row=1, column=0, padx=5, pady=5)
            self.cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('Unavailable', id))
            self.conn.commit()
            self.cursor.execute('INSERT INTO rentals (book_id, quantity, rental_date) VALUES (?, ?, ?)', (id, book[3], datetime.now().strftime('%Y-%m-%d %H:%M')))
            self.conn.commit()
            self.cursor.execute('UPDATE status SET rental = rental + ? WHERE title = ?', (book[3], book[1]))
            self.cursor.execute('UPDATE status SET available = available - ? WHERE title = ?', (quantity, book[1]))
            self.conn.commit()

        else:
            self.cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('Available', id))
            self.conn.commit()
            self.cursor.execute('INSERT INTO rentals (book_id, quantity, rental_date) VALUES (?, ?, ?)', (id, quantity, datetime.now().strftime('%Y-%m-%d %H:%M')))
            self.conn.commit()
            self.cursor.execute('UPDATE status SET rental = rental + ? WHERE title = ?', (quantity, book[1]))
            self.cursor.execute('UPDATE status SET available = available - ? WHERE title = ?', (quantity, book[1]))
            self.conn.commit()

        # 更新图书信息表格
        self.cursor.execute('UPDATE status SET update_date = ? WHERE title = ?', (datetime.now().strftime('%Y-%m-%d %H:%M'), book[1]))
        self.conn.commit()
        self.refresh4()

    def return_book(self):
        id = self.entry_rental_book_id.get()
        quantity = self.entry_return_quantity1.get()
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book = self.cursor.fetchone()
        self.cursor.execute('SELECT * FROM status WHERE title = ?', (book[1],))
        status = self.cursor.fetchone()

        if int(status[4]) - int(quantity) < 0:
            self.label_return_quantity2 = tk.Label(self.tab_rental, text='已全部归还')
            self.label_return_quantity2.grid(row=5, column=0, padx=5, pady=5)
            self.cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('Available', id))
            self.conn.commit()
            self.cursor.execute('INSERT INTO rentals (book_id, quantity, return_date) VALUES (?, ?, ?)', (id, quantity, datetime.now().strftime('%Y-%m-%d %H:%M')))
            self.conn.commit()
            self.cursor.execute('UPDATE status SET rental = rental - ? WHERE title = ?', (0, book[1]))
            self.cursor.execute('UPDATE status SET available = available + ? WHERE title = ?', (quantity, book[1]))
            self.conn.commit()
        else:
            self.cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('Available', id))
            self.conn.commit()
            self.cursor.execute('INSERT INTO rentals (book_id, quantity, return_date) VALUES (?, ?, ?)', (id, quantity, datetime.now().strftime('%Y-%m-%d %H:%M')))
            self.conn.commit()
            self.cursor.execute('UPDATE status SET rental = rental - ? WHERE title = ?', (quantity, book[1]))
            self.cursor.execute('UPDATE status SET available = available + ? WHERE title = ?', (quantity, book[1]))
            self.conn.commit()
 
        self.cursor.execute('UPDATE status SET update_date = ? WHERE title = ?', (datetime.now().strftime('%Y-%m-%d %H:%M'), book[1]))
        self.refresh4()