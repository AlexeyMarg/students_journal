import tkinter as tk
import os
import sqlite3
import tkinter.ttk as ttk


class Application:
    def __init__(self, parent):
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", self._delete_window)
        self.connect_db()
        self.subject_list = self.get_subjects()
        self.subject_var = tk.StringVar()
        self.subject_var.set(self.subject_list[0])
        self.subject_option = tk.OptionMenu(parent, self.subject_var, *self.subject_list)
        self.subject_option.config(width=15)
        self.subject_option.grid(row=1, column=1, padx=2, pady=2)
        self.subject_add_button = tk.Button(parent, text='Add subject', command=self.press_add_subject)
        self.subject_add_button.grid(row=1, column=2, padx=2, pady=2)
        self.subject_del_button = tk.Button(parent, text='Delete subject', command=self.press_del_subject)
        self.subject_del_button.grid(row=1, column=3, padx=2, pady=2)
        self.student_add_button = tk.Button(parent, text='Add student', command=self.press_add_student)
        self.student_add_button.grid(row=1, column=4, padx=2, pady=2)
        self.student_del_button = tk.Button(parent, text='Delete student', command=self.press_del_student)
        self.student_del_button.grid(row=1, column=5, padx=2, pady=2)

        self.subject_headers = self.get_headers(self.subject_var.get())
        self.subject_rows = self.get_rows(self.subject_var.get())
        print(self.subject_rows)

        table = Table(parent, headings=self.subject_headers, rows=self.subject_rows)
        table.grid(row=2, column=1, columnspan=5)


    def connect_db(self):
        dbname = 'database.db'
        path = os.getcwd()
        self.conn = sqlite3.connect(path + '\\' + dbname)
        self.cursor = self.conn.cursor()

    def get_headers(self, table):
        self.cursor.execute('select * from %s' % (table))
        res = []
        for i in self.cursor.description:
            res.append(i[0])
        return res

    def get_rows(self, table):
        self.cursor.execute('select * from %s' % (table))
        res = self.cursor.fetchall()
        return res

    def _delete_window(self):
        self.conn.commit()
        self.conn.close()
        self.parent.destroy()

    def get_subjects(self):
        res = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        subject_list = []
        for name in res:
            subject_list.append(name[0])
        return subject_list

    def press_add_subject(self):
        pass

    def press_del_subject(self):
        pass

    def press_add_student(self):
        pass

    def press_del_student(self):
        pass


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)
