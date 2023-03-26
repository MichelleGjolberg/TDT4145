import sqlite3

#Må hente databasefilen
con = sqlite3.connect("jernbaneDBnynyny.db") 
cursor = con.cursor()

stasjonsNavn = input('Skriv inn stasjon: ')
dag = input('Skriv inn dag: ')

#Her henter vi ut både dersom stasjonen er start-, mellom- eller endestasjon til en rute
query = ('''SELECT DISTINCT Togrute.RuteNr
FROM Togrute 
INNER JOIN MellomstasjonRute ON Togrute.RuteNr = MellomstasjonRute.RuteNr
INNER JOIN StartstasjonRute ON Togrute.RuteNr = StartstasjonRute.RuteNr
INNER JOIN EndestasjonRute ON Togrute.RuteNr = EndestasjonRute.RuteNr
INNER JOIN Kjører ON Togrute.RuteNr = Kjører.RuteNr
WHERE (MellomstasjonRute.StasjonNavn = ? OR StartstasjonRute.StasjonNavn = ? OR EndestasjonRute.StasjonNavn = ?) AND Kjører.Dag = ?
''')

print('Disse togrutene kjører gjennom' , str(stasjonsNavn) ,'på' , str(dag) ,':', cursor.execute(query, (stasjonsNavn, stasjonsNavn, stasjonsNavn, dag))
      .fetchall())

#for row in cursor.fetchall():
    #print(row[0])

con.commit()
con.close()