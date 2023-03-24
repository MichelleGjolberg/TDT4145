import sqlite3
from datetime import datetime

con = sqlite3.connect("jernbaneDBnynyny.db") #Må hente databasefilen

cursor = con.cursor()

# For å kunne teste i databasen
# cursor.execute('''INSERT INTO Sete VALUES (1, True, 'SJ-sittevogn-1-1')''')
# cursor.execute('''INSERT INTO Sete VALUES (2, True, 'SJ-sittevogn-1-1')''')
# cursor.execute('''INSERT INTO Sovekupé VALUES (1, True, 'SJ-sovevogn-1-1')''')
# cursor.execute('''INSERT INTO Sovekupé VALUES (2, True, 'SJ-sovevogn-1-1')''')
# cursor.execute('''INSERT INTO Kundeordre VALUES (1, '2023-02-02', '12:12:00', 1, 1, 1, '2023-04-03')''')
# cursor.execute('''INSERT INTO KjøpAvKupé VALUES (1, 1, 'SJ-sovevogn-1-1')''')
# cursor.execute('''INSERT INTO Kundeordre VALUES (2, '2023-02-02', '12:12:00', 1, 1, 1, '2023-04-03')''')
# cursor.execute('''INSERT INTO KjøpAvSete VALUES (2, 1, 1)''')
# cursor.execute('''INSERT INTO BillettTilDelstrekning VALUES(1, 'Steinkjer-Mosjøen')''')

ruteNr = 1 #input('Skriv inn ønsker togrutenr: ')
kundeNr = 1 #input('Skriv inn ditt kundenr: ')
dato = '2023-04-03' #input('Hvilken dato ønsker du å reise på? (YYYY-MM-DD): ')
startStasjon = 'Trondheim S' #input('Hvilken stasjon skal du reise fra? ')
endeStasjon = 'Mosjøen' #input('Hvilken stasjon skal du reise til? ')
seteEllerSeng = 'sete' #input('Vil du ha sete eller seng: ')

mellomstrekninger = cursor.execute(f'''SELECT DS.FraStasjonNavn, DS.TilSTasjonNavn 
                                        FROM Delstrekning AS DS
                                        INNER JOIN Banestrekning AS BS ON (BS.Navn = DS.BanestrekningNavn)
                                        INNER JOIN Togrute AS TR ON (TR.BanestrekningNavn = BS.Navn)
                                        WHERE TR.RuteNr = {ruteNr}''').fetchall()

#print('Mellomstrekning: ')
#print(mellomstrekninger)

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
    if ((str(mellomstrekninger[i][0]) == startStasjon) & (str(mellomstrekninger[i][1]) == endeStasjon)): #Ingen mellomstasjoner
        break
    if (mellomstrekninger[i][0] == startStasjon):
        check = True
    if (mellomstrekninger[i][1] == endeStasjon): #Avbryter når man har nådd ende stasjonen
        break
    if check:
        mellomstasjoner.append(mellomstrekninger[i][1])

#print('Melomstasjoner: ')
#print(mellomstasjoner)


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

#print('Alle stasjoner: ')
#print(alleStasjoner)

delstrekninger = tuple(str(alleStasjoner[i]) + "-" + 
                       str(alleStasjoner[i+1]) for i in range(0, len(alleStasjoner)-1))

print('Delstrekninger: ')
print(delstrekninger)

if seteEllerSeng == 'sete':
    params = (dato, *delstrekninger, dato)
    delstrekninger_str = [str(elem) for elem in delstrekninger]
    query = '''SELECT COUNT(DISTINCT S.SeteNr), S.SeteNr, VO.VognNr, ST.Avgangstid
    FROM Sete AS S
    INNER JOIN VognIOppsett AS VO ON (VO.VognID = S.VognID)
    INNER JOIN Togrute AS TR ON (TR.OppsettID = VO.OppsettID)
    INNER JOIN Togrutetabell AS TRT ON (TRT.RuteNr = TR.RuteNr)
    INNER JOIN StasjonITabell AS ST ON (ST.TabellNr = ST.TabellNr)
    WHERE S.SeteNr NOT IN (
        SELECT S.SeteNr
        FROM Sete AS S
        INNER JOIN KjøpAvSete AS KS ON (KS.SeteNr = S.SeteNr)
        INNER JOIN Kundeordre AS KO ON (KO.OrdreNr = KS.OrdreNr)
        INNER JOIN Togruteforekomst AS TF ON (TF.Dato = KO.Dato)
        WHERE TF.Dato = ?
    )
    UNION
    SELECT COUNT(DISTINCT S.SeteNr), S.SeteNr, VO.VognNr, ST.Avgangstid
    FROM Sete AS S
    INNER JOIN VognIOppsett AS VO ON (VO.VognID = S.VognID)
    INNER JOIN Togrute AS TR ON (TR.OppsettID = VO.OppsettID)
    INNER JOIN Togrutetabell AS TRT ON (TRT.RuteNr = TR.RuteNr)
    INNER JOIN StasjonITabell AS ST ON (ST.TabellNr = ST.TabellNr)
    WHERE S.SeteNr NOT IN (
        SELECT DISTINCT S.SeteNr
        FROM Sete AS S
        INNER JOIN KjøpAvSete AS KS ON (KS.SeteNr = S.SeteNr)
        INNER JOIN Kundeordre AS KO ON (KO.OrdreNr = KS.OrdreNr)
        INNER JOIN Togruteforekomst AS TF ON (TF.Dato = KO.Dato)
        INNER JOIN BillettTilDelstrekning AS BD ON (BD.OrdreNr = KS.OrdreNr)
        WHERE BD.DelstrekningNavn IN ({}) AND TF.Dato = ?)
    '''.format(','.join('?' for _ in delstrekninger))

elif seteEllerSeng == 'seng': 
    params = (dato)
    query = '''SELECT COUNT(DISTINCT SK.KupéNr), SK.KupéNr, VO.VognNr, ST.Avgangstid
    FROM SoveKupé AS SK 
    INNER JOIN VognIOppsett AS VO ON (VO.VognID = SK.VognID)
    INNER JOIN Togrute AS TR ON (TR.OppsettID = VO.OppsettID)
    INNER JOIN Togrutetabell AS TRT ON (TRT.RuteNr = TR.RuteNr)
    INNER JOIN StasjonITabell AS ST ON (ST.TabellNr = ST.TabellNr)
    WHERE SK.KupéNr NOT IN (
        SELECT SK.KupéNr
        FROM Sovekupé AS SK
        INNER JOIN KjøpAvKupé AS KK ON (KK.KupéNr = SK.KupéNr)
        INNER JOIN Kundeordre AS KO ON (KO.OrdreNr = KS.OrdreNr)
        INNER JOIN Togruteforekomst AS TF ON (TF.Dato = KO.Dato)
        WHERE TF.Dato = ?
    )'''

result = cursor.execute(query, params)
rows = result.fetchall()

print('')
print('Ledige seter på rute-nr. ' + str(ruteNr) + ' fra ' + startStasjon + ' på dato ' + dato + ' er: ')
header = ['BillettNr', 'SeteNr', 'VognNr', 'Avgangstid']
print('-' * (len(header) * 15 + 1))
print('|', end='')
for h in header:
    print(f' {h:<12} |', end='')
print()
print('-' * (len(header) * 15 + 1))
for row in rows:
    print('|', end='')
    for value in rows[i]:
        print(f' {str(value):<12} |', end='')
    print()
print('-' * (len(header) * 15 + 1))
print('')
valid_antall = False
#antar at bruker skriver inn valid antall etter hvert, hvis ikke blir det uendelig loop
while not valid_antall: 
    antall = input('Hvor mange billetter ønsker du å kjøpe?')
    if antall <= len(rows):
        valid_antall = True

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H:%M:%S.%f")

if antall == 0:
    print('Du ønsker ikke å kjøpe noen billetter')
else: 
    nylig_kjøpte = []
    for i in range(1, antall):
        input('Nå skal du få velge billett nr ' + i)
        print('')
        billettNr = input('Hvilken billett ønsker du å kjøpe? \nSkriv inn billettnummeret: ')
        if billettNr not in nylig_kjøpte:
            correct_billettNr = False
            for row in rows:
                if billettNr == row[0]:
                    correct_billettNr = True
            if not correct_billettNr:
                print('Ikke gyldig billettNr')
            else:
                cursor.execute(''''INSERT INTO Kundeordre (DagKjøpt, TidKjøpt, Antall, KundeNr, RuteNr, Dato) VALUES (?, ?, ?, ?, ?, ?)''', 
                            (date, time, antall, kundeNr, ruteNr, dato))
                nylig_kjøpte.append(billettNr)
        else: 
            print('Denne billetten har du allerede kjøpt')


con.commit()
con.close()