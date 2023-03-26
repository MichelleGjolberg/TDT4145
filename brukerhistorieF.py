import sqlite3
from datetime import datetime

con = sqlite3.connect("jernbaneDBdenne.db") #Må hente databasefilen

cursor = con.cursor()

#Legge rinn i togruteforekomst
cursor.execute('''INSERT INTO Togruteforekomst VALUES ('2023-04-04',1)''')
cursor.execute('''INSERT INTO Togruteforekomst VALUES ('2023-04-03',1)''')

cursor.execute('''INSERT INTO Togruteforekomst VALUES ('2023-04-04',2)''')
cursor.execute('''INSERT INTO Togruteforekomst VALUES ('2023-04-03',2)''')

cursor.execute('''INSERT INTO Togruteforekomst VALUES ('2023-04-04',3)''')
cursor.execute('''INSERT INTO Togruteforekomst VALUES ('2023-04-03',3)''')




con.commit()

con.close()

