import sqlite3
con = sqlite3.connect("jernbaneDBnynyny.db") #Må hente databasefilen

cursor = con.cursor()

registrereBoolean = input('Do you want to register Y/N: ') 


if registrereBoolean == 'Y':
    Navn = input('Enter name: ') 
    Epost = input('Enter email: ') 
    MobilNr = input('Enter phonenumber (8 digits): ') 
    while len(MobilNr) != 8 or not MobilNr.isdigit():
        print("Phone number must be 8 digits long and contain only numbers.")
        MobilNr = input('Enter phonenumber (8 digits): ')

    cursor.execute('''INSERT INTO KUNDE (Navn, Epost, MobilNr) VALUES (?, ?, ?)''', (Navn, Epost, MobilNr))  
    KundeNr = cursor.lastrowid


con.commit()
con.close()