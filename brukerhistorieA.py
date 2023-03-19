import sqlite3
con = sqlite3.connect("nydb.db") #Må hente databasefilen

cursor = con.cursor()

#Legger til Banestrekningen
cursor.execute('''INSERT OR IGNORE INTO Banestrekning VALUES ('Norlandsbanen','Diesel','Retning1','Trondheim','Bodø')''')

#Legger til mellomstasjoner
cursor.execute('''INSERT OR IGNORE INTO mellomstasjonBane VALUES ('Norlandsbane','Steinkjer')''')
cursor.execute('''INSERT OR IGNORE INTO mellomstasjonBane VALUES ('Norlandsbane','Mosjøen')''')
cursor.execute('''INSERT OR IGNORE INTO mellomstasjonBane VALUES ('Norlandsbane','Mo i Rana')''')
cursor.execute('''INSERT OR IGNORE INTO mellomstasjonBane VALUES ('Norlandsbane','Fauske')''')

#Legger til jernbanestasjoner
cursor.execute('''INSERT OR IGNORE INTO Jernbanestasjon VALUES ('Steinkjer','3.6')''')
cursor.execute('''INSERT OR IGNORE INTO Jernbanestasjon VALUES ('Trondheim S','5.1')''')
cursor.execute('''INSERT OR IGNORE INTO Jernbanestasjon VALUES ('Mosjøen','6.8')''')
cursor.execute('''INSERT OR IGNORE INTO Jernbanestasjon VALUES ('Mo i Rana','3.5')''')
cursor.execute('''INSERT OR IGNORE INTO Jernbanestasjon VALUES ('Fauske','34.0')''')
cursor.execute('''INSERT OR IGNORE INTO Jernbanestasjon VALUES ('Bodø','4.1')''')

#Legger til delstrekninger
cursor.execute('''INSERT OR IGNORE INTO Delstrekning VALUES ('Trondheim-Steinkjer','120','Dobbeltspor','Trondheim','Steinskjer')''')
cursor.execute('''INSERT OR IGNORE INTO Delstrekning VALUES ('Steinkjer-Mosjøen','280','Dobbeltspor','Steinskjer','Mosjøen')''')
cursor.execute('''INSERT OR IGNORE INTO Delstrekning VALUES ('Mosjøen-Mo i Rana','90','Dobbeltspor','Mosjøen','Mo i Rana')''')
cursor.execute('''INSERT OR IGNORE INTO Delstrekning VALUES ('Mo i Rana-Fauske','170','Dobbeltspor','Mo i Rana','Fauske')''')
cursor.execute('''INSERT OR IGNORE INTO Delstrekning VALUES ('Fauske-Bodø','60','Dobbeltspor','Fauske','Bodø')''')


con.commit()


con.close()

