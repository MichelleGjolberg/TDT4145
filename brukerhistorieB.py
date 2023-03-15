import sqlite3
con = sqlite3.connect("jernbaneDBNY.db") #Må hente databasefilen

cursor = con.cursor()

#Opretter vognopsett, operatør og vogner som kan legges i vognoppsett
cursor.execute('''INSERT INTO Vognoppsett VALUES (1)''')
cursor.execute('''INSERT INTO Operatør VALUES ('SJ')''')
cursor.execute('''INSERT INTO Sittevogn VALUES (12, 'SJ-sittevogn1-1',False,'SJ')''')
cursor.execute('''INSERT INTO Sittevogn VALUES (12, 'SJ-sittevogn1-2',False,'SJ')''')

cursor.execute('''INSERT INTO VognIOppsett VALUES (1, 'SJ-sittevogn1-1',1)''')
cursor.execute('''INSERT INTO VognIOppsett VALUES (2, 'SJ-sittevogn1-2',1)''')

#Legger til Togrute
cursor.execute('''INSERT INTO Togrute VALUES (1,'MedHovedretning','SJ','1','Norlandsbanen')''') #Dagtog Trondheim til Bodø

#Legg til i Togrruteforekomst
cursor.execute('''INSERT INTO Togruteforekomst VALUES ('13.03.22',1)''') #Dagtog Trondheim til Bodø


#Legger til i Rutetabell
cursor.execute('''INSERT INTO Togrutetabell VALUES (1,1)''')

#Legger til startstasjon
cursor.execute('''INSERT INTO StartstasjonRute VALUES ('07:49:00','Trondheim S', 1)''')

#Legger til mellomstasjoner
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('09:51:00.000','09:51:00.00',1, 'Steinskjer')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('13:20:00.00','13:20:00.00',1, 'Mosjøen')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('14:31:00.00','14:31:00.00',1, 'Mo i Rana')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('16:49:00.00','16:49:00.00',1, 'Fauske')''')

#Legger til endestasjon
cursor.execute('''INSERT INTO EndestasjonRute VALUES ('17:34:00',1, 'Bodø')''')

#Legger til i StasjonITabell
cursor.execute('''INSERT INTO StasjonITabell VALUES ('09:51:00.00','09:51:00.00', 'Steinskjer',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('13:20:00.00','13:20:00.00','Mosjøen',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('14:31:00.00','14:31:00.00','Mo i Rana',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('16:49:00.00','16:49:00.00','Fauske',1)''')

con.commit()


con.close()

