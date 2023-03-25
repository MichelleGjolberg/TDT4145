import sqlite3
import datetime

# Må hente databasefilen
con = sqlite3.connect("jernbaneDBnynyny.db") 
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

ruteNr = input('Skriv inn ønsker togrutenr: ')
kundeNr = input('Skriv inn ditt kundenr: ')
dato = input('Hvilken dato ønsker du å reise på? (YYYY-MM-DD): ')
startStasjon = input('Hvilken stasjon skal du reise fra? ')
endeStasjon = input('Hvilken stasjon skal du reise til? ')
seteEllerSeng = input('Vil du ha sete eller seng: ')

# Henter ut alle mellomstrekninger på rutenummeret som er valgt
mellomstrekninger = cursor.execute(f'''SELECT DS.FraStasjonNavn, DS.TilSTasjonNavn 
                                        FROM Delstrekning AS DS
                                        INNER JOIN Banestrekning AS BS ON (BS.Navn = DS.BanestrekningNavn)
                                        INNER JOIN Togrute AS TR ON (TR.BanestrekningNavn = BS.Navn)
                                        WHERE TR.RuteNr = {ruteNr}''').fetchall()

# Henter ut retningen på rutenummeret som er valgt
# Dette for å sjekke om vi må endre retning når vi finner delstrekninger
retning = cursor.execute(f'''SELECT Retning 
                            FROM Togrute 
                            WHERE RuteNr = {ruteNr}''').fetchall()

# Bytter plass hvis retningen er mot hovedretning
if(retning[0][0] == "MotHovedretning"):
    start = startStasjon
    startStasjon = endeStasjon
    endeStasjon = start

# Hente ut alle mellomstasjoner til denne ruten
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

delstrekninger = tuple(str(alleStasjoner[i]) + "-" + 
                       str(alleStasjoner[i+1]) for i in range(0, len(alleStasjoner)-1))

if seteEllerSeng == 'sete':
    params = (dato, *delstrekninger, dato)
    delstrekninger_str = [str(elem) for elem in delstrekninger]
    query = '''SELECT COUNT(DISTINCT S.SeteNr), S.SeteNr, VO.VognNr, VO.VognID, ST.Avgangstid
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
    SELECT COUNT(DISTINCT S.SeteNr), S.SeteNr, VO.VognNr, VO.VognID, ST.Avgangstid
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
    query = '''SELECT COUNT(DISTINCT SK.KupéNr), SK.KupéNr, VO.VognNr, VO.VognID, ST.Avgangstid
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
header = ['BillettNr', 'SeteNr', 'VognNr', 'VognID', 'Avgangstid']
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
    antall = int(input('Hvor mange billetter ønsker du å kjøpe?'))
    if antall <= len(rows):
        valid_antall = True

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H:%M:%S.%f")

if antall == 0:
    print('Du ønsker ikke å kjøpe noen billetter')
else: 
    nylig_kjøpte = []
    kjøpt_samme = False
    for i in range(1, antall+1):
        print('Nå skal du få velge billett nr. ' + str(i))
        print('')
        while not kjøpt_samme:
            billettNr = int(input('Hvilken billett ønsker du å kjøpe? \nSkriv inn billettnummeret: '))
            if billettNr not in nylig_kjøpte:
                billettNr_in_rows = False
                for row in rows:
                    if billettNr == row[0]:
                        billettNr_in_rows = True
                        plass = row[1]
                        vognID = row[3]
                        break
                if not billettNr_in_rows:
                    print('Ikke gyldig billettNr, prøv igjen')
                else:
                    cursor.execute('''INSERT INTO Kundeordre (DagKjøpt, TidKjøpt, Antall, KundeNr, RuteNr, Dato) VALUES (?, ?, ?, ?, ?, ?)''', 
                            (date, time, antall, kundeNr, ruteNr, dato))
                    ordreNr = cursor.lastrowid
                    for delstrekning in delstrekninger:
                        cursor.execute('''INSERT INTO BillettTilDelstrekning VALUES (?, ?)''', 
                                       (ordreNr, delstrekning))
                    if seteEllerSeng == 'sete':
                        cursor.execute('''INSERT INTO KjøpAvSete VALUES (?, ?, ?)''',
                                       (ordreNr, plass, vognID))
                    elif seteEllerSeng == 'seng':
                        cursor.execute('''INSERT INTO KjøpAvKupé VALUES (?, ?, ?)''',
                                       (ordreNr, plass, vognID))
                    nylig_kjøpte.append(billettNr)
                    kjøpt_samme = True
            else: 
                print('Denne billetten har du allerede kjøpt, prøv igjen')

con.commit()
con.close()