import tkinter as tk
import os
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as mb


class Application:
    def __init__(self, parent):
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", self._delete_window)
        self.connect_db()
        self.subject_list = self.get_subjects()
        self.subject_var = tk.StringVar()
        self.subject_var.set(self.subject_list[0])
        self.subject_option = tk.OptionMenu(parent, self.subject_var, *self.subject_list, command=self.subject_selection)
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

        self.table = Table(parent, headings=self.subject_headers, rows=self.subject_rows)
        self.table.grid(row=2, column=1, columnspan=len(self.subject_headers))


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

    def subject_selection(self, event):
        self.table.destroy()
        table = self.subject_var.get()
        headers = self.get_headers(table)
        rows = self.get_rows(table)
        self.subject_headers = headers
        self.subject_rows = rows
        self.table = Table(self.parent, headings=headers, rows=rows)
        self.table.grid(row=2, column=1, columnspan=len(headers))


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
        self.add_subject_window = tk.Toplevel(self.parent)
        self.add_subject_window.title('Add subject')
        self.add_subject_label = tk.Label(self.add_subject_window, text='Enter Name and headings via ,:')
        self.add_subject_label.grid(row=1, column=1, padx=2, pady=2, sticky='w')
        self.add_subject_entry = tk.Entry(self.add_subject_window, width=50)
        self.add_subject_entry.grid(row=2, column=1, padx=2, pady=2)
        self.add_subject_button = tk.Button( self.add_subject_window, text='Add', width=10, command=self.add_subject)
        self.add_subject_button.grid(row=3, column=1, padx=2, pady=2)

    def add_subject(self):
        s = self.add_subject_entry.get().replace(', ', ',').split(sep=',')
        self.cursor.execute('CREATE TABLE %s (Name CHAR(255), Group_number CHAR(255)   )' % (s[0],))
        self.subject_list.append(s[0],)
        self.subject_option['menu'].delete(0, 'end')
        table = s[0]
        s = s[1:]
        for i in s:
            self.cursor.execute('ALTER TABLE %s ADD COLUMN %s INT' % (table, str(i)))
        self.subject_option.destroy()
        self.subject_var.set(self.subject_list[0])
        self.subject_option = tk.OptionMenu(self.parent, self.subject_var, *self.subject_list,
                                            command=self.subject_selection)
        self.subject_option.config(width=15)
        self.subject_option.grid(row=1, column=1, padx=2, pady=2)
        self.add_subject_window.destroy()

    def press_del_subject(self):
        subject = self.subject_var.get()
        answer = mb.askyesno(title="Removing", message="Do you want to remove selected subject?")
        if answer:
            self.cursor.execute("DROP TABLE %s" % (subject,))
            self.subject_list.remove(subject)
            self.subject_option.destroy()
            self.subject_var.set(self.subject_list[0])
            self.subject_option = tk.OptionMenu(self.parent, self.subject_var, *self.subject_list,
                                                command=self.subject_selection)
            self.subject_option.config(width=15)
            self.subject_option.grid(row=1, column=1, padx=2, pady=2)


    def press_add_student(self):
        self.add_student_window = tk.Toplevel(self.parent)
        self.add_student_window.title('Add student')
        self.add_student_label1 = tk.Label(self.add_student_window, text='Enter student data via , for headers:')
        self.add_student_label1.grid(row=1, column=1, padx=2, pady=2, sticky='w')
        s = ''
        for i in self.subject_headers:
            s=s+i+', '
        s = s[:-2]
        self.add_student_label2 = tk.Label(self.add_student_window, text=s)
        self.add_student_label2.grid(row=2, column=1, padx=2, pady=2, sticky='w')
        self.add_student_entry = tk.Entry(self.add_student_window, width=50)
        self.add_student_entry.grid(row=3, column=1, padx=2, pady=2)
        self.add_student_button = tk.Button(self.add_student_window, text='Add', width=10, command=self.add_student)
        self.add_student_button.grid(row=4, column=1, padx=2, pady=2)

    def add_student(self):
        s = self.add_student_entry.get().replace(', ', ',').split(',')
        subject = self.subject_var.get()
        if len(s) != len(self.subject_headers):
            mb.showerror("Error!", "Wrong input data")
        else:
            sql = 'INSERT INTO ' + subject + ' ('
            for i in self.subject_headers[:-1]:
                sql = sql + i + ', '
            sql = sql + self.subject_headers[-1] + ') VALUES ('
            sql = sql + '\'' + s[0] + '\', ' + '\'' + s[1] + '\', '
            for i in s[2:-1]:
                sql = sql + i + ', '
            sql = sql + s[-1] + ')'
            self.cursor.execute(sql)
            self.table.destroy()
            self.subject_headers = self.get_headers(subject)
            self.subject_rows = self.get_rows(subject)
            self.table = Table(self.parent, headings=self.subject_headers, rows=self.subject_rows)
            self.table.grid(row=2, column=1, columnspan=len(self.subject_headers))
            self.add_student_window.destroy()


    def press_del_student(self):
        answer = mb.askyesno(title="Removing", message="Do you want to remove selected student?")
        if answer:
            i = int(self.table.table.selection()[0][-1])
            print(self.subject_rows[i-1][0])
            self.cursor.execute('DELETE FROM %s WHERE Name==\'%s\'' % (self.subject_rows[i-1][0]))


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        self.table = ttk.Treeview(self, show="headings", selectmode="browse")
        self.table["columns"] = headings
        self.table["displaycolumns"] = headings

        for head in headings:
            self.table.heading(head, text=head, anchor=tk.CENTER)
            self.table.column(head, anchor=tk.CENTER)

        for row in rows:
            self.table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
