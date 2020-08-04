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

print("Table created successfully........")

conn.commit()
conn.close()