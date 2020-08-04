import sqlite3
import os

dbname = 'database.db'

path = os.getcwd()
conn = sqlite3.connect(path+'\\'+dbname)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Subject1")
cursor.execute("DROP TABLE IF EXISTS Subject2")

sql ='''CREATE TABLE Subject1(
   Name CHAR(255),
   Group_number CHAR(255),
   Task1 INT,
   Task2 INT,
   Exam INT
)'''
cursor.execute(sql)

sql ='''CREATE TABLE Subject2(
   Name CHAR(255),
   Group_number CHAR(255),
   Task1 INT,
   Task2 INT,
   Task3 INT,
   Exam INT
)'''
cursor.execute(sql)

print("Tables created successfully")

cursor.execute('''insert into Subject1 (Name, Group_number, Task1, Task2, Exam) values
                    ('Smith', 'R1', 2, 3, 0) ''')
cursor.execute('''insert into Subject2 (Name, Group_number, Task1, Task2, Task3,  Exam) values
                    ('Ivanov', 'R2', 2, 3, 3, 5) ''')
cursor.execute('''insert into Subject2 (Name, Group_number, Task1, Task2, Task3,  Exam) values
                    ('Petrov', 'R2', 5, 3, 3, 4) ''')
print("Data inserted successfully")

print('Names in Subject1:')
cursor.execute('SELECT Name FROM Subject1')
result = cursor.fetchall()
for i in result:
    print(i[0])
print('Names in Subject2:')
cursor.execute('SELECT Name FROM Subject2')
result = cursor.fetchall()
for i in result:
    print(i[0])



conn.commit()
conn.close()