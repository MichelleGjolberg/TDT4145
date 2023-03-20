import sqlite3
con = sqlite3.connect("testDB3.db") #Må hente databasefilen

cursor = con.cursor()


stasjonsNavn = input('Skriv inn stasjon: ')
dag = input('Skriv inn dag: ')



query = ('''SELECT Togrute.RuteNr
FROM Togrute 
INNER JOIN MellomstasjonRute ON Togrute.RuteNr = MellomstasjonRute.RuteNr
INNER JOIN StartstasjonRute ON Togrute.RuteNr = StartstasjonRute.RuteNr
INNER JOIN Kjører ON Togrute.RuteNr = Kjører.RuteNr
WHERE MellomstasjonRute.StasjonNavn = ? AND Kjører.Dag = ?
''')





print('Disse togrutene kjører gjennom' , str(stasjonsNavn) ,'på' , str(dag) ,':', cursor.execute(query, (stasjonsNavn, dag))
      .fetchall())



for row in cursor.fetchall():
    print(row[0])



con.commit()
con.close()