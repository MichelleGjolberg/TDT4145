import sqlite3
from datetime import datetime

<<<<<<< HEAD
con = sqlite3.connect("jernbaneDBdenne.db") #Må hente databasefilen

=======
con = sqlite3.connect("jernbaneDBnynyny.db") #Må hente databasefilen
>>>>>>> 6c2bb70b625b9796a4ff139f7ae1c7333c4653c4
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

