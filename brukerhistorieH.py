import sqlite3
from datetime import datetime

con = sqlite3.connect("testDB3.db") #Må hente databasefilen

cursor = con.cursor()

#Spørre om kundenr
kundeNr = input('Hva er ditt KundeNr?')
res = cursor.execute(f"SELECT * FROM Kundeordre WHERE KundeNr = {kundeNr} ")  
result = res.fetchall()

#hente ut dagens dato
date = datetime.today()

#Henter ut alle ordre fra kunden som er i dag eller senere
togruteInfo = cursor.execute(f'''SELECT RuteNr, Retning, BanestrekningNavn,od.OrdreNr, od.KundeNr, 
od.Antall,  od.Dato, od.startStasjon, od.endeStasjon  FROM Togrute NATURAL JOIN 
(SELECT ko.OrdreNr, ko.Antall, ko.KundeNr, tf.RuteNr, tf.Dato , ko.startStasjon, ko.endeStasjon 
FROM Kundeordre AS ko INNER JOIN Togruteforekomst AS tf 
WHERE ko.RuteNr = tf.RuteNr AND ko.Dato = tf.Dato AND ko.KundeNr = {kundeNr}) AS od WHERE od.Dato >= "{date}"''') 
togruteres =togruteInfo.fetchall()

for j in range(0,len(togruteres)):
            print("\n------------ Ordre: " + str(togruteres[j][3]) + "------------ ")
            print("\nAntall plasser: " + str(togruteres[j][5]) + ", \nBane: " + str(togruteres[j][2]) + "\nRetning: " + str(togruteres[j][1]) + ", \nRute nummer: "+ str(togruteres[j][0]) + ", \nDato: "+ str(togruteres[j][6]))

            #Henter ut alle stasjoner med tider
            print("Du/Dere reiser fra: " + str(togruteres[j][7]))
            print("Du/Dere reiser til: " + str(togruteres[j][8]))
            print("\nOversikt over ankomst/angangstider:")
            startInfo = cursor.execute(f"SELECT StasjonNavn, Avgangstid FROM StartstasjonRute WHERE RuteNr = {togruteres[j][0]}")
            startStasjon = startInfo.fetchall()

            endeInfo = cursor.execute(f"SELECT StasjonNavn, Ankomsttid FROM EndestasjonRute WHERE RuteNr = {togruteres[j][0]}")
            endeStasjon = endeInfo.fetchall()

            mellomInfo = cursor.execute(f"SELECT StasjonNavn, Ankomsttid, Avgangstid FROM mellomstasjonRute WHERE RuteNr = {togruteres[j][0]}")
            mellomstasjoner = mellomInfo.fetchall()

            print("\n\Stasjon | Stasjons navn | Ankomsttid | Avgangstid ")
            print("Start   | " + str(startStasjon[0][0]) + " |  | " +str(startStasjon[0][1]))
            
            for t in range (0, len(mellomstasjoner)):
                print("Mellom  | " + str(mellomstasjoner[t][0]) + " | " +str(mellomstasjoner[t][1]) + " | " +str(mellomstasjoner[t][2]))

            print("Ende    | " + str(endeStasjon[0][0]) + " | " +str(endeStasjon[0][1]) + " |")

            #Henter ut alle plassreservasjonene
            seteInfo = cursor.execute(f"SELECT VognID, VognNr, ko.OrdreNr, ko.RuteNr, ko.Dato, ko.SeteNr FROM VognIOppsett NATURAL JOIN (SELECT *  FROM Kundeordre NATURAL JOIN KjøpAvSete WHERE OrdreNr = {togruteres[j][3]} ) AS ko  ")
            seteRes = seteInfo.fetchall()

            soveInfo  = cursor.execute(f"SELECT VognID, VognNr, ko.OrdreNr, ko.RuteNr, ko.Dato, ko.KupéNr FROM VognIOppsett NATURAL JOIN (SELECT *  FROM Kundeordre NATURAL JOIN KjøpAvKupé WHERE OrdreNr = {togruteres[j][3]}) AS ko ")
            soveRes = soveInfo.fetchall()
           
            if(len(seteRes) > 0):
                print("\nMed disse sitteplassene: ")
                for k in range( 0, len(seteRes)):
                    print("Vogn nummer: " + str(seteRes[k][1]) + ", Setenummer: " + str(seteRes[k][5]))
            
            if(len(soveRes) > 0):
                print("\nMed disse sovekupé plassene: ") 
                for k in range( 0, len(soveRes)):
                    print("Vogn nummer: " + str(soveRes[k][1]) + ", Kupénummer: " + str(soveRes[k][5]))
            
            print("\n--------------------------------- ")        

con.commit()

con.close()

