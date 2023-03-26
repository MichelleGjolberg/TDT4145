import sqlite3
<<<<<<< HEAD
con = sqlite3.connect("jernbaneDBdenne.db") #Må hente databasefilen
=======
con = sqlite3.connect("jernbaneDBnynyny.db") #Må hente databasefilen
>>>>>>> 6c2bb70b625b9796a4ff139f7ae1c7333c4653c4

cursor = con.cursor()

#Legger til Banestrekningen
<<<<<<< HEAD
cursor.execute('''INSERT INTO Banestrekning VALUES ('Nordlandsbanen','Diesel','Retning1','Trondheim S','Bodø')''')
=======
cursor.execute('''INSERT INTO Banestrekning VALUES ('Nordlandsbanen','Diesel','Retning1','Trondheim','Bodø')''')
>>>>>>> 6c2bb70b625b9796a4ff139f7ae1c7333c4653c4

#Legger til mellomstasjoner
cursor.execute('''INSERT INTO mellomstasjonBane VALUES ('Nordlandsbanen','Steinkjer')''')
cursor.execute('''INSERT INTO mellomstasjonBane VALUES ('Nordlandsbanen','Mosjøen')''')
cursor.execute('''INSERT INTO mellomstasjonBane VALUES ('Nordlandsbanen','Mo i Rana')''')
cursor.execute('''INSERT INTO mellomstasjonBane VALUES ('Nordlandsbanen','Fauske')''')

#Legger til jernbanestasjoner
cursor.execute('''INSERT INTO Jernbanestasjon VALUES ('Steinkjer','3.6')''')
cursor.execute('''INSERT INTO Jernbanestasjon VALUES ('Trondheim S','5.1')''')
cursor.execute('''INSERT INTO Jernbanestasjon VALUES ('Mosjøen','6.8')''')
cursor.execute('''INSERT INTO Jernbanestasjon VALUES ('Mo i Rana','3.5')''')
cursor.execute('''INSERT INTO Jernbanestasjon VALUES ('Fauske','34.0')''')
cursor.execute('''INSERT INTO Jernbanestasjon VALUES ('Bodø','4.1')''')

#Legger til delstrekninger
<<<<<<< HEAD
cursor.execute('''INSERT INTO Delstrekning VALUES ('Trondheim S-Steinkjer','120','Dobbeltspor','Trondheim S','Steinkjer', 'Nordlandsbanen')''')
=======
cursor.execute('''INSERT INTO Delstrekning VALUES ('Trondheim-Steinkjer','120','Dobbeltspor','Trondheim','Steinskjer', 'Nordlandsbanen')''')
>>>>>>> 6c2bb70b625b9796a4ff139f7ae1c7333c4653c4
cursor.execute('''INSERT INTO Delstrekning VALUES ('Steinkjer-Mosjøen','280','Dobbeltspor','Steinskjer','Mosjøen', 'Nordlandsbanen')''')
cursor.execute('''INSERT INTO Delstrekning VALUES ('Mosjøen-Mo i Rana','90','Dobbeltspor','Mosjøen','Mo i Rana', 'Nordlandsbanen')''')
cursor.execute('''INSERT INTO Delstrekning VALUES ('Mo i Rana-Fauske','170','Dobbeltspor','Mo i Rana','Fauske', 'Nordlandsbanen')''')
cursor.execute('''INSERT INTO Delstrekning VALUES ('Fauske-Bodø','60','Dobbeltspor','Fauske','Bodø', 'Nordlandsbanen')''')


con.commit()


con.close()

