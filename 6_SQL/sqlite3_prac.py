import sqlite3

connect = sqlite3.connect("temp.db");

cursor = connect.cursor();

cursor.execute('CREATE TABLE TEST_TABLE(name text, age interger)');
