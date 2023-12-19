import tkinter as tk
import sqlite3
import random
from tkinter import ttk
from datetime import datetime

class Book:

    def create_random_books(self, num=20):
        """随机创建图书"""
        for i in range(num):
            title = 'Book' + str(i+1)
            author = 'Author' + str(i+1)
            quantity = random.randint(0, 100)
            status = 'Available'
            self.cursor.execute('INSERT INTO books (title, author, quantity, status) VALUES (?, ?, ?, ?)', (title, author, quantity, status))
            # 时间精确到分钟
            self.cursor.execute('INSERT INTO status (title, available, unavailable, rental, update_date) VALUES (?, ?, ?, ?, ?)', (title, quantity, 0, 0, datetime.now().strftime('%Y-%m-%d %H:%M')))
        self.conn.commit()