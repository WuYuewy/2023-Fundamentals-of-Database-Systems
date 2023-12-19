# GUI

import tkinter as tk
import sqlite3
import random
from tkinter import ttk
from datetime import datetime

class GUI:
    def __init__(self, root):
        self.init_database()
        self.init_style()
        self.root = root
        self.root.title("图书管理系统")
        self.root.geometry('400x300')
        self.root.resizable(0, 0)
        self.init_database()
        
        label = tk.Label(root, text="图书管理系统")
        label.pack()
        button1 = tk.Button(root, text="状态查询", command=self.show_statics)
        button1.pack()
        button2 = tk.Button(root, text="图书管理", command=self.operate_books)
        button2.pack()
        #排版
        label.place(x=150, y=50, width=100, height=50)
        button1.place(x=150, y=100, width=100, height=50)
        button2.place(x=150, y=170, width=100, height=50)
        
    def init_style(self):
        # 设置颜色等ui
        style = ttk.Style()
        style.configure("Treeview", font=('Times New Roman', 12))
        style.configure("Treeview.Heading", font=('Times New Roman', 14, 'bold'))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.configure("TNotebook", font=('Times New Roman', 12))
        style.configure("TNotebook.Tab", font=('Times New Roman', 12))
        style.configure("TButton", font=('Times New Roman', 12))
        style.configure("TLabel", font=('Times New Roman', 12))

        #设置背景颜色为浅黄色
        style.configure("TNotebook", background="lightyellow")
        style.configure("TNotebook.Tab", background="lightyellow")
        style.configure("TButton", background="lightyellow")
        # 设置popup背景为浅蓝色
        style.configure("Toplevel", background="black")

    def show_statics(self):

        popup1 = tk.Toplevel()
        popup1.geometry('800x500')
        # 固定窗口大小
        popup1.resizable(0, 0)
        label = tk.Label(popup1, text="馆内图书状况查询界面")
        label.pack()

        # 创建Notebook
        self.notebook = ttk.Notebook(popup1)
        self.notebook.pack(pady=10)
        self.notebook.place(x=0, y=50, width=800, height=600)

        # 创建各个标签页
        self.tab_books = ttk.Frame(self.notebook)
        self.tab_purchase = ttk.Frame(self.notebook)
        self.tab_retire = ttk.Frame(self.notebook)
        self.tab_rental = ttk.Frame(self.notebook)
        self.tab_statistics = ttk.Frame(self.notebook)

        self.tab_books.place(x=0, y=50, width=800, height=600)
        self.tab_purchase.place(x=0, y=50, width=800, height=600)
        self.tab_retire.place(x=0, y=50, width=800, height=600)
        self.tab_rental.place(x=0, y=50, width=800, height=600)
        self.tab_statistics.place(x=0, y=50, width=800, height=600)

        # 添加标签页到Notebook
        self.notebook.add(self.tab_books, text="图书信息")
        self.notebook.add(self.tab_purchase, text="采购记录")
        self.notebook.add(self.tab_retire, text="淘汰记录")
        self.notebook.add(self.tab_rental, text="租借记录")
        self.notebook.add(self.tab_statistics, text="统计信息")

        # 初始化数据库和表格
        
        self.init_book_tab()
        self.init_purchase_query_tab()
        self.init_retire_query_tab()
        self.init_rental_query_tab()
        self.init_statistics_tab()

    def operate_books(self):

        popup2 = tk.Toplevel()
        popup2.geometry('400x300')
        popup2.resizable(0, 0)
        label = tk.Label(popup2, text="馆内图书状况管理界面")
        label.pack()

        # 创建Notebook
        self.notebook = ttk.Notebook(popup2)
        self.notebook.pack(pady=10)
        self.notebook.place(x=0, y=50, width=700, height=500)

        # 创建各个标签页
        self.tab_purchase = ttk.Frame(self.notebook)
        self.tab_retire = ttk.Frame(self.notebook)
        self.tab_rental = ttk.Frame(self.notebook)
        self.tab_statistics = ttk.Frame(self.notebook)

        self.tab_purchase.place(x=0, y=50, width=700, height=500)
        self.tab_retire.place(x=0, y=50, width=800, height=600)
        self.tab_rental.place(x=0, y=50, width=800, height=600)

        # 添加标签页到Notebook
        self.notebook.add(self.tab_purchase, text="图书采购")
        self.notebook.add(self.tab_retire, text="图书淘汰")
        self.notebook.add(self.tab_rental, text="图书租借/归还")

        # 初始化数据库和表格
        self.init_purchase_tab()
        self.init_retire_tab()
        self.init_rental_tab()