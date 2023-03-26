import sqlite3
<<<<<<< HEAD
con = sqlite3.connect("jernbaneDBdenne.db") #Må hente databasefilen
=======

#Må hente databasefilen
con = sqlite3.connect("jernbaneDBnynyny.db") 
>>>>>>> 6c2bb70b625b9796a4ff139f7ae1c7333c4653c4
cursor = con.cursor()

#Legger til dager
cursor.execute('''INSERT INTO Dag VALUES ("Mandag")''')
cursor.execute('''INSERT INTO Dag VALUES ("Tirsdag")''')
cursor.execute('''INSERT INTO Dag VALUES ("Onsdag")''')
cursor.execute('''INSERT INTO Dag VALUES ("Torsdag")''')
cursor.execute('''INSERT INTO Dag VALUES ("Fredag")''')
cursor.execute('''INSERT INTO Dag VALUES ("Lørdag")''')
cursor.execute('''INSERT INTO Dag VALUES ("Søndag")''')

#Opretter vognopsett, operatør og vogner som kan legges i vognoppsett
cursor.execute('''INSERT INTO Vognoppsett VALUES (1)''')
cursor.execute('''INSERT INTO Operatør VALUES ('SJ')''')
cursor.execute('''INSERT INTO Sittevogn VALUES (12, 'SJ-sittevogn1-1',False,'SJ')''')
cursor.execute('''INSERT INTO Sittevogn VALUES (12, 'SJ-sittevogn1-2',False,'SJ')''')
cursor.execute('''INSERT INTO VognIOppsett VALUES (1,'SJ-sittevogn1-1',1)''')
cursor.execute('''INSERT INTO VognIOppsett VALUES (2,'SJ-sittevogn1-2',1)''')
cursor.execute('''INSERT INTO Vognoppsett VALUES (2)''')
cursor.execute('''INSERT INTO Sittevogn VALUES (12, 'SJ-sittevogn1-3',False,'SJ')''')
cursor.execute('''INSERT INTO Sovevogn VALUES (4, 'SJ-sovevogn1-1',False,'SJ')''')
cursor.execute('''INSERT INTO VognIOppsett VALUES (1,'SJ-sittevogn1-3',2)''')
cursor.execute('''INSERT INTO VognIOppsett VALUES (2,'SJ-sovevogn1-1',2)''')
cursor.execute('''INSERT INTO Vognoppsett VALUES (3)''')
cursor.execute('''INSERT INTO Sittevogn VALUES (12, 'SJ-sittevogn1-4',False,'SJ')''')
cursor.execute('''INSERT INTO VognIOppsett VALUES (1,'SJ-sittevogn1-4',3)''')

#Legger til seter og soveplasser

SittevognerType1 = ['SJ-sittevogn1-1','SJ-sittevogn1-2','SJ-sittevogn1-3','SJ-sittevogn1-4']

for i in range(0, len(SittevognerType1)):

    for j in range(0,13):
        cursor.execute(f'''INSERT INTO Sete VALUES ({j},{SittevognerType1[i]})''')

SovevognerType1 = ['SJ-sovevogn1-1']

for i in range(0, len(SovevognerType1)):
    
    for j in range(0,5):
        cursor.execute(f'''INSERT INTO Sovekupé VALUES ({j},{SovevognerType1[i]})''')

#Legger til Togrute
cursor.execute('''INSERT INTO Togrute VALUES (1,'MedHovedretning','SJ','1','Nordlandsbanen')''') #Dagtog Trondheim til Bodø
cursor.execute('''INSERT INTO Togrute VALUES (2,'MedHovedretning','SJ','2','Nordlandsbanen')''') #Natttog Trondheim til Bodø
cursor.execute('''INSERT INTO Togrute VALUES (3,'MotHovedretning','SJ','3','Nordlandsbanen')''') #Morgetog MO i Rana til Trondheim
#Legegr til dager ruten kjører
cursor.execute('''INSERT INTO Kjører VALUES ("Mandag",1)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Tirsdag",1)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Onsdag",1)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Torsdag",1)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Fredag",1)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Mandag",2)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Tirsdag",2)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Onsdag",2)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Torsdag",2)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Fredag",2)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Lørdag",2)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Søndag",2)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Mandag",3)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Tirsdag",3)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Onsdag",3)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Torsdag",3)''')
cursor.execute('''INSERT INTO Kjører VALUES ("Fredag",3)''')

#Legger til i Rutetabell
cursor.execute('''INSERT INTO Togrutetabell VALUES (1,1)''')
cursor.execute('''INSERT INTO Togrutetabell VALUES (2,2)''')
cursor.execute('''INSERT INTO Togrutetabell VALUES (3,3)''')

#Legger til startstasjon
cursor.execute('''INSERT INTO StartstasjonRute VALUES ('07:49:00','Trondheim S', 1)''')
cursor.execute('''INSERT INTO StartstasjonRute VALUES ('23:05:00','Trondheim S', 2)''')
cursor.execute('''INSERT INTO StartstasjonRute VALUES ('08:11:00','Mo i Rana', 3)''')

#Legger til mellomstasjoner
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('09:51:00.000','09:51:00.00',1, 'Steinkjer')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('13:20:00.00','13:20:00.00',1, 'Mosjøen')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('14:31:00.00','14:31:00.00',1, 'Mo i Rana')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('16:49:00.00','16:49:00.00',1, 'Fauske')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('00:57:00.000','00:57:00.000',2, 'Steinkjer')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('04:41:00.00','04:41:00.00',2, 'Mosjøen')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('05:55:00.00','05:55:00.00',2, 'Mo i Rana')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('08:19:00.00','08:19:00.00',2, 'Fauske')''')
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('09:14:00.00','09:14:00.00',3, 'Mosjøen')''')
<<<<<<< HEAD
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('12:31:00.000','12:31:00.000',3, 'Steinkjer')''')
=======
cursor.execute('''INSERT INTO MellomstasjonRute VALUES ('12:31:00.000','12:31:00.000',3, 'Steinskjer')''')

>>>>>>> 6c2bb70b625b9796a4ff139f7ae1c7333c4653c4
#Legger til endestasjon
cursor.execute('''INSERT INTO EndestasjonRute VALUES ('17:34:00','Bodø', 1)''')
cursor.execute('''INSERT INTO EndestasjonRute VALUES ('09:05:00', 'Bodø', 2)''')
cursor.execute('''INSERT INTO EndestasjonRute VALUES ('14:13:00','Trondheim S', 3)''')

#Legger til i StasjonITabell
cursor.execute('''INSERT INTO StasjonITabell VALUES ('07:49:00.00','07:49:00.00', 'Trondheim S',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('09:51:00.00','09:51:00.00', 'Steinkjer',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('13:20:00.00','13:20:00.00','Mosjøen',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('14:31:00.00','14:31:00.00','Mo i Rana',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('16:49:00.00','16:49:00.00','Fauske',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('17:34:00.00','17:34:00.00', 'Bodø',1)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('23:05:00.00','23:05:00.00', 'Trondheim S',2)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('00:57:00.000','00:57:00.000', 'Steinkjer',2)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('04:41:00.00','04:41:00.00','Mosjøen',2)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('05:55:00.00','05:55:00.00','Mo i Rana',2)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('08:19:00.00','08:19:00.00','Fauske',2)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('09:05:00.00','09:05:00.00', 'Bodø',2)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('08:11:00','08:11:00','Mo i Rana', 3)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('09:14:00.00','09:14:00.00', 'Mosjøen',3)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('12:31:00.000','12:31:00.000', 'Steinkjer',3)''')
cursor.execute('''INSERT INTO StasjonITabell VALUES ('14:13:00','14:13:00', 'Trondheim S',3)''')

con.commit()
con.close()