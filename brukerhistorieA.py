import sqlite3
con = sqlite3.connect("jernbaneDBnynyny.db") #Må hente databasefilen

cursor = con.cursor()

#Legger til Banestrekningen
cursor.execute('''INSERT INTO Banestrekning VALUES ('Nordlandsbanen','Diesel','Retning1','Trondheim','Bodø')''')

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
cursor.execute('''INSERT INTO Delstrekning VALUES ('Trondheim-Steinkjer','120','Dobbeltspor','Trondheim','Steinskjer', 'Nordlandsbanen')''')
cursor.execute('''INSERT INTO Delstrekning VALUES ('Steinkjer-Mosjøen','280','Dobbeltspor','Steinskjer','Mosjøen', 'Nordlandsbanen')''')
cursor.execute('''INSERT INTO Delstrekning VALUES ('Mosjøen-Mo i Rana','90','Dobbeltspor','Mosjøen','Mo i Rana', 'Nordlandsbanen')''')
cursor.execute('''INSERT INTO Delstrekning VALUES ('Mo i Rana-Fauske','170','Dobbeltspor','Mo i Rana','Fauske', 'Nordlandsbanen')''')
cursor.execute('''INSERT INTO Delstrekning VALUES ('Fauske-Bodø','60','Dobbeltspor','Fauske','Bodø', 'Nordlandsbanen')''')


con.commit()


con.close()

