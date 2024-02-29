import sqlite3

banco = sqlite3.connect('database.db')

cursor = banco.cursor()

#cursor.execute("INSERT INTO Pessoa VALUES (154, 'Carlos Rocha', '12345678910', 'carlos.rocha@riogrande.ifrs.edu.br', 1)")
#banco.commit()
cursor.execute("SELECT Papel FROM Pessoa WHERE Nome = 'Carlos Rocha'")
#cursor.execute("SELECT 
print(cursor.fetchall())