import tkinter as tk
import sqlite3
import random
from tkinter import ttk
from datetime import datetime

class PurchaseSystem: 

    def purchase_book1(self):
        id = self.entry_purchase_book_id.get()
        quantity = self.entry_purchase_quantity1.get()

        # 更新图书数量和状态
        self.cursor.execute('UPDATE books SET quantity = quantity + ? WHERE id = ?', (quantity, id))
        self.cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('Available', id))
        self.conn.commit()

        # 插入采购记录
        self.cursor.execute('INSERT INTO purchases (book_id, quantity, purchase_date) VALUES (?, ?, ?)', (id, quantity, datetime.now().strftime('%Y-%m-%d %H:%M')))
        self.conn.commit()
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book = self.cursor.fetchone()
        self.cursor.execute('UPDATE status SET available = ? WHERE title = ?', (book[3], book[1]))
        self.cursor.execute('UPDATE status SET update_date = ? WHERE title = ?', (datetime.now().strftime('%Y-%m-%d %H:%M'), book[1]))
        self.conn.commit()
        self.refresh1()

    def purchase_book2(self):
        title = self.entry_purchase_title2.get()
        author = self.entry_purchase_author2.get()
        quantity = self.entry_purchase_quantity3.get()
        status = 'Available'

        # 插入新的图书信息（包括书名、作者、状态）
        self.cursor.execute('INSERT INTO books (title, author, quantity, status) VALUES (?, ?, ?, ?)', (title, author, quantity, status))
        self.conn.commit()

        # 插入采购记录
        self.cursor.execute('INSERT INTO purchases (book_id, quantity, purchase_date) VALUES (?, ?, ?)', (self.cursor.lastrowid, quantity, datetime.now().strftime('%Y-%m-%d %H:%M')))
        self.conn.commit()

        # 更新图书信息表格
        # self.update_book_table()
        # 更新统计信息表格
        self.cursor.execute('INSERT INTO status (title, available, unavailable, rental, update_date) VALUES (?, ?, ?, ?, ?)', (title, quantity, 0, 0, datetime.now().strftime('%Y-%m-%d %H:%M')))
        self.conn.commit()

        # 刷新页面
        self.refresh2()