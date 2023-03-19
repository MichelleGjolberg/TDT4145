import sqlite3
con = sqlite3.connect("nydb.db") #Må hente databasefilen

cursor = con.cursor()

#cursor.execute('''INSERT INTO Togrute VALUES ('1', 'MedHovedretning', 'SVJ', '2', 'Nordlandsbanen')''')
#cursor.execute('''INSERT INTO Togruteforekomst VALUES ('10.10.22', 1)''')
#cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('10:10:00','10:11:00', '1', 'Mosjøen' )''')
#cursor.execute('''INSERT INTO StartstasjonRute VALUES ('10:09:00', '1', 'Bodø' )''')
#cursor.execute('''INSERT INTO Togruteforekomst VALUES ('10.10.22', 1)''')
cursor.execute('''INSERT INTO Dag VALUES ('Tirsdag')''')

stasjonsNavn = input('Enter station name: ')
dato = input('Enter date: ')
dag = input('Enter dag: ')


query = ('''SELECT *
FROM Togrute 
INNER JOIN MellomstasjonRute ON Togrute.RuteNr = MellomstasjonRute.RuteNr
INNER JOIN StartstasjonRute ON Togrute.RuteNr = StartstasjonRute.RuteNr
INNER JOIN TogruteForekomst ON Togrute.RuteNr = TogruteForekomst.RuteNr
WHERE MellomstasjonRute.StasjonNavn = ? AND Dag.Dag = ?
''')
        
         


print()
print(cursor.execute(query, (stasjonsNavn,dato)))


for row in cursor.fetchall():
    print(row[0])



con.commit()
con.close()

