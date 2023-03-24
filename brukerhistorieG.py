import sqlite3
from datetime import datetime

con = sqlite3.connect("jernbaneDBnynyny.db") #Må hente databasefilen

cursor = con.cursor()

# Prøveverdier for sete og sovekupe, trenger nok ikke men sletter ikke i tilfelle
# cursor.execute('''INSERT INTO Sete VALUES (1, True, 'SJ-sittevogn-1-1')''')
# cursor.execute('''INSERT INTO Sete VALUES (2, True, 'SJ-sittevogn-1-1')''')
# cursor.execute('''INSERT INTO Sovekupé VALUES (1, True, 'SJ-sovevogn-1-1')''')
# cursor.execute('''INSERT INTO Sovekupé VALUES (2, True, 'SJ-sovevogn-1-1')''')
# cursor.execute('''INSERT INTO SovekupéPåForekomst VALUES (1, True, 'SJ-sovevogn-1-1', '2023-04-03', 1)''')
# cursor.execute('''INSERT INTO SovekupéPåForekomst VALUES (2, True, 'SJ-sovevogn-1-1', '2023-04-03', 1)''')
# cursor.execute('''INSERT INTO SovekupéPåForekomst VALUES (1, True, 'SJ-sovevogn-1-1', '2023-04-04', 1)''')
# cursor.execute('''INSERT INTO SovekupéPåForekomst VALUES (2, True, 'SJ-sovevogn-1-1', '2023-04-04', 1)''')
# cursor.execute('''INSERT INTO SetePåForekomst VALUES (1, True, 'SJ-sovevogn-1-1', '2023-04-03', 1, "Trondheim S", "Mosjøen")''')
# cursor.execute('''INSERT INTO SetePåForekomst VALUES (2, True, 'SJ-sovevogn-1-1', '2023-04-03', 1, "Trondheim S", "Mosjøen")''')
# cursor.execute('''INSERT INTO SetePåForekomst VALUES (1, True, 'SJ-sovevogn-1-1', '2023-04-04', 1, "Trondheim S", "Mosjøen")''')
# cursor.execute('''INSERT INTO SetePåForekomst VALUES (2, True, 'SJ-sovevogn-1-1', '2023-04-04', 1, "Trondheim S", "Mosjøen")''')


# bruker disse
# cursor.execute('''INSERT INTO Kundeordre VALUES (1, '2023-02-02', '12:12:00', 1, 1, 1, '2023-04-03')''')
# cursor.execute('''INSERT INTO KjøpAvKupé VALUES (1, 1, 'SJ-sovevogn-1-1')''')
#cursor.execute('''INSERT INTO Kundeordre VALUES (2, '2023-02-02', '12:12:00', 1, 1, 1, '2023-04-03')''')
#cursor.execute('''INSERT INTO KjøpAvSete VALUES (2, 1, 1)''')


#togrute = input('Skriv inn ønsker togrutenr: ')
#kundenr = input('Skriv inn ditt kundenr: ')
#fra = input('Hvilken stasjon skal du reise fra? ')
#til = input('Hvilken stasjon skal du reise til? ')
seteEllerSeng = input('Vil du ha sete eller seng: ')

# fraTest = ""
# params = (fra, til)
# #while (fraTest != fra):
# finnStartDelstrekning = '''SELECT DS.Navn
#     FROM Jernbanestasjon AS JS
#     INNER JOIN Delstrekning AS DS ON (JS.Navn = DS.FraStasjonNavn)
#     WHERE JS.Navn LIKE ?
#     UNION
#     SELECT DS.Navn
#     FROM Jernbanestasjon AS JS
#     INNER JOIN Delstrekning AS DS ON (JS.Navn = DS.TilStasjonNavn)
#     WHERE JS.Navn = ?
#     '''
#     #fraTest = fra

#print(cursor.execute(finnStartDelstrekning, params).fetchall())

ruteNr = 3 #input('Hvilken rute ønsker du å reise med?: ')
dato = "2023-04-04" #input(Hvilken dato ønsker du å reise på? (YYYY-MM-DD): )
startStasjon = "Steinkjer" #input('Hvor starter din reise?: ')
endeStasjon = "Trondheim S" #input('Hvor ender din reise?: ')

mellomstrekninger = cursor.execute(f'''SELECT DS.FraStasjonNavn, DS.TilSTasjonNavn 
                                        FROM Delstrekning AS DS
                                        INNER JOIN Banestrekning AS BS ON (BS.Navn = DS.BanestrekningNavn)
                                        INNER JOIN Togrute AS TR ON (TR.BanestrekningNavn = BS.Navn)
                                        WHERE TR.RuteNr = {ruteNr}''').fetchall()

retning = cursor.execute(f'''SELECT Retning 
                            FROM Togrute 
                            WHERE RuteNr = {ruteNr}''').fetchall()

if(retning[0][0] == "MotHovedretning"):
    #Bytter plass siden det er i mot hovedretning
    start = startStasjon
    startStasjon = endeStasjon
    endeStasjon = start

#Hente ut alle mellomstasjoner til denne ruten
mellomstasjoner = []

check = False
for i in range(0,len(mellomstrekninger)):
    #for j in range(0, len(mellomstrekninger[i])):
    if ((str(mellomstrekninger[i][0]) == startStasjon) & (str(mellomstrekninger[i][1]) == endeStasjon)): #Ingen mellomstasjoner
        break
    if (mellomstrekninger[i][0] == startStasjon):
        check = True
    if (mellomstrekninger[i][1] == endeStasjon): #Avbryter når man har nådd ende stasjonen
        break
    if check:
        mellomstasjoner.append(mellomstrekninger[i][1])


# if (retning[0][0] == "MotHovedretning"):
#     Bytter tilbake og snur mellomstasjoner
#     start = startStasjon
#     startStasjon = endeStasjon
#     endeStasjon = start
#     mellomstasjoner.reverse()

alleStasjoner = []
alleStasjoner.append(startStasjon)

for i in range(0, len(mellomstasjoner)):
    alleStasjoner.append(mellomstasjoner[i])

alleStasjoner.append(endeStasjon)

# delstrekninger = []
# for i in range(0, len(alleStasjoner)-1):
#     delstrekninger.append(str(alleStasjoner[i]) + "-" + str(alleStasjoner[i+1]))

delstrekninger = tuple(str(alleStasjoner[i]) + "-" + str(alleStasjoner[i+1]) for i in range(0, len(alleStasjoner)-1))

params = ([dato], delstrekninger, [dato])

if seteEllerSeng == 'sete':
    delstrekninger_str = [str(elem) for elem in delstrekninger]
    query = '''SELECT *
    FROM Sete AS S
    WHERE S.SeteNr NOT IN (
        SELECT S.SeteNr
        FROM Sete AS S
        INNER JOIN KjøpAvSete AS KS ON (KS.SeteNr = S.SeteNr)
        INNER JOIN Kundeordre AS KO ON (KO.OrdreNr = KS.OrdreNr)
        INNER JOIN Togruteforekomst AS TF ON (TF.Dato = KO.Dato)
        WHERE TF.Dato = ?
    )
    UNION
    SELECT *
    FROM Sete AS S
    WHERE S.SeteNr NOT IN (
        SELECT S.SeteNr
        FROM Sete AS S
        INNER JOIN KjøpAvSete AS KS ON (KS.SeteNr = S.SeteNr)
        INNER JOIN Kundeordre AS KO ON (KO.OrdreNr = KS.OrdreNr)
        INNER JOIN Togruteforekomst AS TF ON (TF.Dato = KO.Dato)
        INNER JOIN BillettTilDelstrekning AS BD ON (BD.OrdreNr = KS.OrdreNr)
        WHERE BD.DelstrekningNavn IN ({}) AND TF.Dato = ?)
    '''.format(', '.join('?' for _ in {delstrekninger}))

if seteEllerSeng == 'seng': 
    query = '''SELECT *
    FROM SoveKupé AS SK 
    WHERE SK.KupéNr NOT IN (
        SELECT SK.KupéNr
        FROM Sovekupé AS SK
        INNER JOIN KjøpAvKupé AS KK ON (KK.KupéNr = SK.KupéNr)
        INNER JOIN Kundeordre AS KO ON (KO.OrdreNr = KS.OrdreNr)
        INNER JOIN Togruteforekomst AS TF ON (TF.Dato = KO.Dato)
    )'''

result = cursor.execute(query, params)
rows = result.fetchall()
print(rows)

con.commit()
con.close()