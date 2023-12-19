import tkinter as tk
import sqlite3
import random
from tkinter import ttk
from datetime import datetime

class LibraryManagementSystem:
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

    def init_book_tab(self):
        self.tree_books = ttk.Treeview(self.tab_books, columns=('ID', 'Title', 'Author', 'Quantity', 'Status'), show='headings')
        self.tree_books.heading('ID', text='ID')
        self.tree_books.heading('Title', text='Title')
        self.tree_books.heading('Author', text='Author')
        self.tree_books.heading('Quantity', text='Quantity')
        self.tree_books.heading('Status', text='Status')

        self.tree_books.column('ID', width=50, minwidth=50, anchor="center")
        self.tree_books.column('Title', width=100, minwidth=100, anchor="center")
        self.tree_books.column('Author', width=100, minwidth=100, anchor="center")
        self.tree_books.column('Quantity', width=100, minwidth=100, anchor="center")
        self.tree_books.column('Status', width=100, minwidth=100, anchor="center")

        self.tree_books.place(x=0, y=0, width=100, height=400)

        self.tree_books.pack()

        # 查询图书信息并插入表格
        self.update_book_table()

    def init_purchase_query_tab(self):
        self.button_search = tk.Button(self.tab_purchase, text='Refresh', command=self.refresh)
        self.button_search.grid(row=0, column=2, padx=5, pady=5)  
        self.purchase_book_exhibit()

    def refresh(self):
        self.update_book_table()
        self.update_statistics_table()
        self.purchase_book_exhibit()


    def init_purchase_tab(self):
        self.label_purchase_book_id = tk.Label(self.tab_purchase, text='Book ID')
        self.label_purchase_book_id.grid(row=0, column=0, padx=5, pady=5)  

        self.entry_purchase_book_id = tk.Entry(self.tab_purchase)
        self.entry_purchase_book_id.grid(row=0, column=1, padx=5, pady=5)  

        self.button_search = tk.Button(self.tab_purchase, text='Search', command=self.book_search)
        self.button_search.grid(row=0, column=2, padx=5, pady=5)  


    def book_search(self):
        id = self.entry_purchase_book_id.get()
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book = self.cursor.fetchone()

        if hasattr(self, 'label_purchase_quantity1'):
            self.label_purchase_quantity1.destroy()
            self.entry_purchase_quantity1.destroy()
            self.button_purchase1.destroy()
        if hasattr(self, 'label_purchase_quantity2'):
            self.label_purchase_quantity2.destroy()
            self.label_purchase_title2.destroy()
            self.entry_purchase_title2.destroy()
            self.label_purchase_author2.destroy()
            self.entry_purchase_author2.destroy()
            self.label_purchase_quantity3.destroy()
            self.entry_purchase_quantity3.destroy()
            self.button_purchase2.destroy()

        if book:
            # 如果图书存在，则更新图书数量和状态
            self.label_purchase_quantity1 = tk.Label(self.tab_purchase, text='图书存在请输入购买的数量')
            self.label_purchase_quantity1.grid(row=1, column=1, padx=5, pady=5)
            self.entry_purchase_quantity1 = tk.Entry(self.tab_purchase)
            self.entry_purchase_quantity1.grid(row=2, column=1, padx=5, pady=5)
            
            # 更新图书数量和状态
            self.button_purchase1 = tk.Button(self.tab_purchase, text='购买', command=self.purchase_book1)
            self.button_purchase1.grid(row=2, column=2, padx=5, pady=5)

        else:
            # 如果图书不存在，则插入新的图书信息（包括书名、作者、状态）
            self.label_purchase_quantity2 = tk.Label(self.tab_purchase, text='图书不存在请输入图书信息')
            self.label_purchase_quantity2.grid(row=1, column=1, padx=5, pady=5)
            self.label_purchase_title2 = tk.Label(self.tab_purchase, text='标题')
            self.label_purchase_title2.grid(row=2, column=0, padx=5, pady=5)
            self.entry_purchase_title2 = tk.Entry(self.tab_purchase)
            self.entry_purchase_title2.grid(row=2, column=1, padx=5, pady=5)

            self.label_purchase_author2 = tk.Label(self.tab_purchase, text='作者')
            self.label_purchase_author2.grid(row=3, column=0, padx=5, pady=5)
            self.entry_purchase_author2 = tk.Entry(self.tab_purchase)
            self.entry_purchase_author2.grid(row=3, column=1, padx=5, pady=5)

            self.label_purchase_quantity3 = tk.Label(self.tab_purchase, text='数量')
            self.label_purchase_quantity3.grid(row=4, column=0, padx=5, pady=5)
            self.entry_purchase_quantity3 = tk.Entry(self.tab_purchase)
            self.entry_purchase_quantity3.grid(row=4, column=1, padx=5, pady=5)

            self.button_purchase2 = tk.Button(self.tab_purchase, text='购买', command=self.purchase_book2)
            self.button_purchase2.grid(row=4, column=2, padx=5, pady=5)

    def purchase_book_exhibit(self):   
        # 如果已经存在则删除
        if hasattr(self, 'tree_purchases'):
            self.tree_purchases.destroy()

        # 展示采购记录
        self.tree_purchases = ttk.Treeview(self.tab_purchase, columns=('ID', 'Book ID', 'Quantity', 'Purchase Date'), show='headings')
        self.tree_purchases.heading('ID', text='ID')
        self.tree_purchases.heading('Book ID', text='Book ID')
        self.tree_purchases.heading('Quantity', text='Quantity')
        self.tree_purchases.heading('Purchase Date', text='Purchase Date')

        self.tree_purchases.column('ID', width=50, minwidth=50, anchor="center")
        self.tree_purchases.column('Book ID', width=100, minwidth=100, anchor="center")
        self.tree_purchases.column('Quantity', width=100, minwidth=100, anchor="center")
        self.tree_purchases.column('Purchase Date', width=100, minwidth=100, anchor="center")

        self.tree_purchases.place(x=100, y=0, width=600, height=400)

        #self.tree_purchases.grid(row=0, column=3, padx=5, pady=5, rowspan=3)

        # 查询采购记录并插入表格
        self.cursor.execute('SELECT * FROM purchases')
        purchases = self.cursor.fetchall()
        for purchase in purchases:
            self.tree_purchases.insert('', 'end', values=purchase)

    def refresh1(self):
        """在完成一次采购后，删除页面所有元素，重新生成输入框"""
        self.label_purchase_book_id.destroy()
        self.entry_purchase_book_id.destroy()
        self.button_search.destroy()

        self.label_purchase_quantity1.destroy()
        self.entry_purchase_quantity1.destroy()
        self.button_purchase1.destroy()

        self.init_purchase_tab()
    
    def refresh2(self):
        """在完成一次采购后，删除页面所有元素，重新生成输入框"""
        self.label_purchase_book_id.destroy()
        self.entry_purchase_book_id.destroy()
        self.button_search.destroy()

        
        self.label_purchase_quantity2.destroy()
        self.label_purchase_title2.destroy()
        self.entry_purchase_title2.destroy()
        self.label_purchase_author2.destroy()
        self.entry_purchase_author2.destroy()
        self.label_purchase_quantity3.destroy()
        self.entry_purchase_quantity3.destroy()
        self.button_purchase2.destroy()

        self.init_purchase_tab()

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

    def init_retire_tab(self):

        self.label_retire_book_id = tk.Label(self.tab_retire, text='Book ID')
        self.label_retire_book_id.grid(row=0, column=0, padx=5, pady=5)

        self.entry_retire_book_id = tk.Entry(self.tab_retire)
        self.entry_retire_book_id.grid(row=0, column=1, padx=5, pady=5)

        self.button_search_retire = tk.Button(self.tab_retire, text='Search', command=self.book_search_retire)
        self.button_search_retire.grid(row=0, column=2, padx=5, pady=5)

    def init_retire_query_tab(self):
        self.button_search_retire = tk.Button(self.tab_retire, text='Refresh', command=self.refresh)
        self.button_search_retire.grid(row=0, column=2, padx=5, pady=5)
        self.retire_book_exhibit()

    def book_search_retire(self):
        id = self.entry_retire_book_id.get()
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        # 统计书籍种类数
        book = self.cursor.fetchone()
        self.cursor.execute('SELECT COUNT(*) FROM books')
        num = self.cursor.fetchone()
        if hasattr(self, 'label_retire_quantity2'):
            self.label_retire_quantity2.destroy()
        if hasattr(self, 'label_retire_quantity3'):
            self.label_retire_quantity3.destroy()
        if hasattr(self, 'label_retire_quantity1'):
            self.label_retire_quantity1.destroy()
            self.entry_retire_quantity1.destroy()
            self.button_retire1.destroy()
        if num[0]+1 > int(id) and int(id)!=0:
            if book[3]:
                # 如果图书存在，则更新图书数量和状态
                self.label_retire_quantity1 = tk.Label(self.tab_retire, text='图书'+id+'存在请输入淘汰的数量')
                self.label_retire_quantity1.grid(row=1, column=1, padx=5, pady=5)
                self.entry_retire_quantity1 = tk.Entry(self.tab_retire)
                self.entry_retire_quantity1.grid(row=2, column=1, padx=5, pady=5)
                
                # 更新图书数量和状态
                self.button_retire1 = tk.Button(self.tab_retire, text='淘汰', command=self.retire_book)
                self.button_retire1.grid(row=2, column=2, padx=5, pady=5)

            else:
                # 如果图书不存在，则提示图书不存在
                self.label_retire_quantity2 = tk.Label(self.tab_retire, text='图书'+id+'不存在')
                self.label_retire_quantity2.grid(row=1, column=1, padx=5, pady=5)
        else:
            self.label_retire_quantity2 = tk.Label(self.tab_retire, text='图书'+id+'不存在')
            self.label_retire_quantity2.grid(row=1, column=1, padx=5, pady=5)

    def retire_book_exhibit(self):
        # 如果已经存在则删除
        if hasattr(self, 'tree_retires'):
            self.tree_retires.destroy()

        # 展示淘汰记录
        self.tree_retires = ttk.Treeview(self.tab_retire, columns=('ID', 'Book ID', 'Quantity', 'Retire Date'), show='headings')
        self.tree_retires.heading('ID', text='ID')
        self.tree_retires.heading('Book ID', text='Book ID')
        self.tree_retires.heading('Quantity', text='Quantity')
        self.tree_retires.heading('Retire Date', text='Retire Date')

        self.tree_retires.column('ID', width=50, minwidth=50, anchor="center")
        self.tree_retires.column('Book ID', width=100, minwidth=100, anchor="center")
        self.tree_retires.column('Quantity', width=100, minwidth=100, anchor="center")
        self.tree_retires.column('Retire Date', width=100, minwidth=100, anchor="center")
        self.tree_retires.place(x=100, y=0, width=600, height=400)

        # 查询淘汰记录并插入表格
        self.cursor.execute('SELECT * FROM retirements')
        retirements = self.cursor.fetchall()
        for retirement in retirements:
            self.tree_retires.insert('', 'end', values=retirement)

    def refresh3(self):
        """在完成一次淘汰后，删除页面所有元素，重新生成输入框"""
        self.label_retire_book_id.destroy()
        self.entry_retire_book_id.destroy()
        self.button_search_retire.destroy()

        self.label_retire_quantity1.destroy()
        self.entry_retire_quantity1.destroy()
        self.button_retire1.destroy()

        self.init_retire_tab()

    def retire_book(self):
        id = self.entry_retire_book_id.get()
        quantity = self.entry_retire_quantity1.get()
        print(id, quantity)

        # 更新图书数量和状态,首先判断淘汰后的数量是否小于0，如果小于0则提示书籍数量不足
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book = self.cursor.fetchone()
        if int(book[3]) - int(quantity) < 0:
            self.label_retire_quantity3 = tk.Label(self.tab_retire, text='书籍数量不足,已全部淘汰')
            self.label_retire_quantity3.grid(row=1, column=0, padx=5, pady=5)
            self.cursor.execute('UPDATE books SET quantity = ? WHERE id = ?', (0, id))
            self.cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('Unavailable', id))
            self.conn.commit()
            self.cursor.execute('INSERT INTO retirements (book_id, quantity, retirement_date) VALUES (?, ?, ?)', (id, book[3], datetime.now().strftime('%Y-%m-%d %H:%M')))
            self.conn.commit()
            self.cursor.execute('UPDATE status SET unavailable = ? WHERE title = ?', (book[3], book[1]))
            self.cursor.execute('UPDATE status SET available = ? WHERE title = ?', (0, book[1]))
            self.conn.commit()
        else:
            self.cursor.execute('UPDATE books SET quantity = quantity - ? WHERE id = ?', (quantity, id))
            self.cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('Available', id))
            self.conn.commit()
            self.cursor.execute('INSERT INTO retirements (book_id, quantity, retirement_date) VALUES (?, ?, ?)', (id, quantity, datetime.now().strftime('%Y-%m-%d %H:%M')))
            self.conn.commit()
            self.cursor.execute('UPDATE status SET unavailable = ? WHERE title = ?', (quantity, book[1]))
            self.cursor.execute('UPDATE status SET available = available - ? WHERE title = ?', (quantity, book[1]))
            self.conn.commit()

        self.refresh3()

    def init_rental_query_tab(self):

        self.button_search_rental = tk.Button(self.tab_rental, text='Refresh', command=self.refresh)
        self.button_search_rental.grid(row=0, column=2, padx=5, pady=5)

        # 展示租借记录
        self.rental_book_exhibit()

    def init_rental_tab(self):
        self.label_rental_book_id = tk.Label(self.tab_rental, text='Book ID')
        self.label_rental_book_id.grid(row=0, column=0, padx=5, pady=5)
        self.entry_rental_book_id = tk.Entry(self.tab_rental)
        self.entry_rental_book_id.grid(row=0, column=1, padx=5, pady=5)
        self.button_search_rental = tk.Button(self.tab_rental, text='Search', command=self.book_search_rental)
        self.button_search_rental.grid(row=0, column=2, padx=5, pady=5)

    def book_search_rental(self):

        if hasattr(self, 'label_rental_quantity2'):
            self.label_rental_quantity2.destroy()
        if hasattr(self, 'label_return_quantity2'):
            self.label_return_quantity2.destroy()
        if hasattr(self, 'label_rental_quantity1'):

            self.label_rental_quantity1.destroy()
            self.entry_rental_quantity1.destroy()
            self.button_rental1.destroy()

            # 归还按钮消除
            self.label_return_quantity1.destroy()
            self.entry_return_quantity1.destroy()
            self.button_return1.destroy()

            self.label_rental_quantity2.destroy()
            self.label_rental_quantity3.destroy()
        
        id = self.entry_rental_book_id.get()
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        try:
            book = self.cursor.fetchone()
            self.cursor.execute('SELECT * FROM status WHERE title = ?', (book[1],))
            status = self.cursor.fetchone()
        except:
            self.label_rental_quantity2 = tk.Label(self.tab_rental, text='图书'+id+'不存在')
            self.label_rental_quantity2.grid(row=1, column=1, padx=5, pady=5)
            return

        if book[3] :
            # 如果图书存在，则更新图书数量和状态
            self.label_rental_quantity1 = tk.Label(self.tab_rental, text='图书'+id+'存在，请输入租借的数量')
            self.label_rental_quantity1.grid(row=1, column=1, padx=5, pady=5)
            self.entry_rental_quantity1 = tk.Entry(self.tab_rental)
            self.entry_rental_quantity1.grid(row=2, column=1, padx=5, pady=5)

            # 目前已经借出的数量
            self.label_rental_quantity2 = tk.Label(self.tab_rental, text='目前已经借出的数量')
            self.label_rental_quantity2.grid(row=3, column=1, padx=5, pady=5)
            self.label_rental_quantity3 = tk.Label(self.tab_rental, text=status[4])
            self.label_rental_quantity3.grid(row=3, column=2, padx=5, pady=5)
            
            # 归还按钮
            self.label_return_quantity1 = tk.Label(self.tab_rental, text='请输入归还的数量')
            self.label_return_quantity1.grid(row=4, column=0, padx=5, pady=5)
            self.entry_return_quantity1 = tk.Entry(self.tab_rental)
            self.entry_return_quantity1.grid(row=4, column=1, padx=5, pady=5)
            self.button_return1 = tk.Button(self.tab_rental, text='归还', command=self.return_book)
            self.button_return1.grid(row=4, column=2, padx=5, pady=5)

            # 更新图书数量和状态
            self.button_rental1 = tk.Button(self.tab_rental, text='租借', command=self.rental_book1)
            self.button_rental1.grid(row=2, column=2, padx=5, pady=5)

        else:
            # 如果图书不存在，则提示图书不存在
            self.label_rental_quantity2 = tk.Label(self.tab_rental, text='图书'+id+'不存在')
            self.label_rental_quantity2.grid(row=1, column=1, padx=5, pady=5)

    def rental_book_exhibit(self):
        # 如果已经存在则删除
        if hasattr(self, 'tree_rentals'):
            self.tree_rentals.destroy()

        # 展示租借记录
        self.tree_rentals = ttk.Treeview(self.tab_rental, columns=('ID', 'Book ID', 'Quantity', 'Rental Date', 'Return Date'), show='headings')
        self.tree_rentals.heading('ID', text='ID')
        self.tree_rentals.heading('Book ID', text='Book ID')
        self.tree_rentals.heading('Quantity', text='Quantity')
        self.tree_rentals.heading('Rental Date', text='Rental Date')
        self.tree_rentals.heading('Return Date', text='Return Date')

        self.tree_rentals.column('ID', width=50, minwidth=50, anchor="center")
        self.tree_rentals.column('Book ID', width=100, minwidth=100, anchor="center")
        self.tree_rentals.column('Quantity', width=100, minwidth=100, anchor="center")
        self.tree_rentals.column('Rental Date', width=100, minwidth=100, anchor="center")
        self.tree_rentals.column('Return Date', width=100, minwidth=100, anchor="center")

        self.tree_rentals.place(x=100, y=0, width=600, height=400)

        # 查询租借记录并插入表格
        self.cursor.execute('SELECT * FROM rentals')
        rentals = self.cursor.fetchall()
        for rental in rentals:
            self.tree_rentals.insert('', 'end', values=rental)

    def refresh4(self):
        self.label_rental_book_id.destroy()
        self.entry_rental_book_id.destroy()
        self.button_search_rental.destroy()

        self.label_rental_quantity1.destroy()
        self.entry_rental_quantity1.destroy()
        self.button_rental1.destroy()

        # 归还按钮消除
        self.label_return_quantity1.destroy()
        self.entry_return_quantity1.destroy()
        self.button_return1.destroy()

        self.label_rental_quantity2.destroy()
        self.label_rental_quantity3.destroy()


        self.init_rental_tab()

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

    def run(self):
        self.root.mainloop()

# 创建主窗口
root = tk.Tk()
app = LibraryManagementSystem(root)
app.run()
