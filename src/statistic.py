import tkinter as tk
import sqlite3
import random
from tkinter import ttk
from datetime import datetime

class LibraryManagementSystem:

    def init_statistics_tab(self):

        self.label_statistics_total = tk.Label(self.tab_statistics, text='书籍总量')
        self.label_statistics_total.grid(row=1, column=0, padx=5, pady=5)
        self.cursor.execute('SELECT SUM(quantity) FROM books')
        total = self.cursor.fetchone()
        self.label_statistics_total_num = tk.Label(self.tab_statistics, text=int(total[0]))
        self.label_statistics_total_num.grid(row=1, column=1, padx=50, pady=5)

        self.label_statistics_available = tk.Label(self.tab_statistics, text='仓库中书籍总量')
        self.label_statistics_available.grid(row=1, column=2, padx=5, pady=5)
        self.cursor.execute('SELECT SUM(available) FROM status')
        available = self.cursor.fetchone()
        self.label_statistics_available_num = tk.Label(self.tab_statistics, text=int(available[0]))
        self.label_statistics_available_num.grid(row=1, column=3, padx=50, pady=5)

        self.label_statistics_rental = tk.Label(self.tab_statistics, text='已借出书籍总量')
        self.label_statistics_rental.grid(row=1, column=4, padx=5, pady=5)
        self.cursor.execute('SELECT SUM(rental) FROM status')
        rental = self.cursor.fetchone()
        self.label_statistics_rental_num = tk.Label(self.tab_statistics, text=rental[0])
        self.label_statistics_rental_num.grid(row=1, column=5, padx=5, pady=5)
        
        self.label_statistics_unavailable = tk.Label(self.tab_statistics, text='已淘汰书籍总量')
        self.label_statistics_unavailable.grid(row=1, column=6, padx=5, pady=5)
        self.cursor.execute('SELECT SUM(unavailable) FROM status')
        unavailable = self.cursor.fetchone()
        self.label_statistics_unavailable_num = tk.Label(self.tab_statistics, text=unavailable[0])
        self.label_statistics_unavailable_num.grid(row=1, column=7, padx=5, pady=5)

        self.label_statistics_update_date = tk.Label(self.tab_statistics, text='最近一次更新时间')
        self.label_statistics_update_date.grid(row=2, column=2, padx=5, pady=5)
        self.cursor.execute('SELECT MAX(update_date) FROM status')
        update_date = self.cursor.fetchone()
        self.label_statistics_update_date_num = tk.Label(self.tab_statistics, text=update_date[0])
        self.label_statistics_update_date_num.grid(row=2, column=3, padx=5, pady=5)

        self.label_statistics_num = tk.Label(self.tab_statistics, text='书籍种类数')
        self.label_statistics_num.grid(row=2, column=5, padx=5, pady=5)
        self.cursor.execute('SELECT COUNT(*) FROM books')
        num = self.cursor.fetchone()
        self.label_statistics_num_num = tk.Label(self.tab_statistics, text=num[0])
        self.label_statistics_num_num.grid(row=2, column=6, padx=5, pady=5)

        # 展示统计信息表格
        self.tree_statistics = ttk.Treeview(self.tab_statistics, columns=('ID', 'Title', 'Available', 'Unavailable', 'Rental', 'Update Date'), show='headings')
        self.tree_statistics.heading('ID', text='ID')
        self.tree_statistics.heading('Title', text='Title')
        self.tree_statistics.heading('Available', text='Available')
        self.tree_statistics.heading('Unavailable', text='Unavailable')
        self.tree_statistics.heading('Rental', text='Rental')
        self.tree_statistics.heading('Update Date', text='Update Date')

        self.tree_statistics.column('ID', width=50, minwidth=50, anchor="center")
        self.tree_statistics.column('Title', width=100, minwidth=100, anchor="center")
        self.tree_statistics.column('Available', width=100, minwidth=100, anchor="center")
        self.tree_statistics.column('Unavailable', width=100, minwidth=100, anchor="center")
        self.tree_statistics.column('Rental', width=100, minwidth=100, anchor="center")
        self.tree_statistics.column('Update Date', width=120, minwidth=100, anchor="center")
        self.tree_statistics.place(x=100, y=70, width=600, height=300)

        # 查询统计信息并插入表格
        self.cursor.execute('SELECT * FROM status')
        status = self.cursor.fetchall()
        for s in status:
            self.tree_statistics.insert('', 'end', values=s)
    
    def update_statistics_table(self):
        # 查询统计信息
        self.cursor.execute('SELECT * FROM status')
        status = self.cursor.fetchall()

        # 清空表格
        for row in self.tree_statistics.get_children():
            self.tree_statistics.delete(row)

        # 插入新数据
        for s in status:
            self.tree_statistics.insert('', 'end', values=s)

        # 更新统计信息
        self.cursor.execute('SELECT SUM(quantity) FROM books')
        total = self.cursor.fetchone()
        self.label_statistics_total_num.config(text=total[0])

        self.cursor.execute('SELECT SUM(available) FROM status')
        available = self.cursor.fetchone()
        self.label_statistics_available_num.config(text=available[0])

        self.cursor.execute('SELECT SUM(rental) FROM status')
        rental = self.cursor.fetchone()
        self.label_statistics_rental_num.config(text=rental[0])

        self.cursor.execute('SELECT SUM(unavailable) FROM status')
        unavailable = self.cursor.fetchone()
        self.label_statistics_unavailable_num.config(text=unavailable[0])

        self.cursor.execute('SELECT MAX(update_date) FROM status')
        update_date = self.cursor.fetchone()
        self.label_statistics_update_date_num.config(text=update_date[0])

        self.cursor.execute('SELECT COUNT(*) FROM books')
        num = self.cursor.fetchone()
        self.label_statistics_num_num.config(text=num[0])

    def update_book_table(self):
        # 查询图书信息
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()

        # 清空表格
        for row in self.tree_books.get_children():
            self.tree_books.delete(row)

        # 插入新数据
        for book in books:
            self.tree_books.insert('', 'end', values=book)