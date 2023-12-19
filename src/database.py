import tkinter as tk
import sqlite3
import random
from tkinter import ttk
from datetime import datetime

class Database:
    def init_database(self):
        # 连接到SQLite数据库
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()

        # 创建图书表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                quantity INTEGER,
                status TEXT    
            )
        ''')

        # 创建采购记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                quantity INTEGER,
                purchase_date DATE,
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')

        # 创建淘汰记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS retirements (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                quantity INTEGER,
                retirement_date DATE,
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')

        # 创建租借记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                quantity INTEGER,
                rental_date DATE,
                return_date DATE,
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')
        # 创建图书状态表（图书名称，可操作（本），淘汰（本），外借（本），更新时间）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS status (
                id INTEGER PRIMARY KEY,
                title TEXT,
                available INTEGER,
                unavailable INTEGER,
                rental INTEGER,
                update_date DATE
            )
        ''')
        if self.cursor.execute('SELECT * FROM books').fetchall() == []:
            self.create_random_books()
        # 提交更改
        self.conn.commit()