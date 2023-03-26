import sqlite3
import datetime

# Må hente databasefilen
con = sqlite3.connect("jernbaneDBdenne.db") 
cursor = con.cursor()

ruteNr = 1 #input('Skriv inn ønsker togrutenr: ')
kundeNr = 1 #input('Skriv inn ditt kundenr: ')
dato = "2023-04-03"#input('Hvilken dato ønsker du å reise på? (YYYY-MM-DD): ')
startStasjon = "Trondheim S"#input('Hvilken stasjon skal du reise fra? ')
endeStasjon = "Mosjøen"#input('Hvilken stasjon skal du reise til? ')
seteEllerSeng = "seng"#input('Vil du ha sete eller seng: ')

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

    # Ingen mellomstasjoner dersom første stasjon er start og siste stasjon er ende
    if ((str(mellomstrekninger[i][0]) == startStasjon) & (str(mellomstrekninger[i][1]) == endeStasjon)): 
        break

    # Setter i gang å legge til i mellomstasjoner når man har nådd startstasjonen
    if (mellomstrekninger[i][0] == startStasjon): 
        check = True

    # Avbryter når man har nådd ende stasjonen    
    if (mellomstrekninger[i][1] == endeStasjon): 
        break

    if check:
        mellomstasjoner.append(mellomstrekninger[i][1])

# Ønsker å bruke alle stasjoner til å finne alle delstrekninger
# Bruker dette dersom bruker ønsker å kjøpe et sette (må sjekke for overlapping)
alleStasjoner = []

# Legger til startstasjonen
alleStasjoner.append(startStasjon)

# Legger til alle mellomstasjoner
for i in range(0, len(mellomstasjoner)):
    alleStasjoner.append(mellomstasjoner[i])

# Legger til endestasjonen
alleStasjoner.append(endeStasjon)

# Finner alle delstrekninger
delstrekninger = tuple(str(alleStasjoner[i]) + "-" + 
                       str(alleStasjoner[i+1]) for i in range(0, len(alleStasjoner)-1))

# Skiller mellom kjøp av sete og seng
if seteEllerSeng == 'sete':
    params = (startStasjon, dato, startStasjon, *delstrekninger, dato)
    delstrekninger_str = [str(elem) for elem in delstrekninger]
    query = '''SELECT COUNT(DISTINCT S.SeteNr), S.SeteNr, VO.VognNr, VO.VognID, ST.Avgangstid
    FROM Sete AS S
    INNER JOIN VognIOppsett AS VO ON (VO.VognID = S.VognID)
    INNER JOIN Togrute AS TR ON (TR.OppsettID = VO.OppsettID)
    INNER JOIN Togrutetabell AS TRT ON (TRT.RuteNr = TR.RuteNr)
    INNER JOIN StasjonITabell AS ST ON (TRT.TabellNr = ST.TabellNr)
    WHERE ST.StasjonNavn = ? AND S.SeteNr NOT IN (
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
    INNER JOIN StasjonITabell AS ST ON (TRT.TabellNr = ST.TabellNr)
    WHERE ST.StasjonNavn = ? AND S.SeteNr NOT IN (
        SELECT DISTINCT S.SeteNr
        FROM Sete AS S
        INNER JOIN KjøpAvSete AS KS ON (KS.SeteNr = S.SeteNr)
        INNER JOIN Kundeordre AS KO ON (KO.OrdreNr = KS.OrdreNr)
        INNER JOIN Togruteforekomst AS TF ON (TF.Dato = KO.Dato)
        INNER JOIN BillettTilDelstrekning AS BD ON (BD.OrdreNr = KS.OrdreNr)
        WHERE BD.DelstrekningNavn IN ({}) AND TF.Dato = ?)
    '''.format(','.join('?' for _ in delstrekninger))

elif seteEllerSeng == 'seng': 
    params = (startStasjon, dato)
    query = '''SELECT ROW_NUMBER() OVER (ORDER BY SK.KupéNr) AS row_num, SK.KupéNr, VO.VognNr, VO.VognID, ST.Avgangstid
    FROM SoveKupé AS SK 
    INNER JOIN VognIOppsett AS VO ON (VO.VognID = SK.VognID)
    INNER JOIN Togrute AS TR ON (TR.OppsettID = VO.OppsettID)
    INNER JOIN Togrutetabell AS TRT ON (TRT.RuteNr = TR.RuteNr)
    INNER JOIN StasjonITabell AS ST ON (TRT.TabellNr = ST.TabellNr)
    WHERE ST.StasjonNavn = ? AND SK.KupéNr NOT IN (
        SELECT SK2.KupéNr
        FROM Sovekupé AS SK2
        INNER JOIN KjøpAvKupé AS KK ON (KK.KupéNr = SK2.KupéNr)
        INNER JOIN Kundeordre AS KO ON (KO.OrdreNr = KK.OrdreNr)
        INNER JOIN Togruteforekomst AS TF ON (TF.Dato = KO.Dato)
        WHERE TF.Dato = ?)
    GROUP BY SK.KupéNr, VO.VognNr, VO.VognID, ST.Avgangstid'''

result = cursor.execute(query, params)
rows = result.fetchall()

# Printer resultattabellen i en tabell
print('')
print('Ledige seter på rute-nr. ' + str(ruteNr) + ' fra ' + startStasjon + ' på dato ' + dato + ' er: ')
if seteEllerSeng == 'sete':
    header = ['BillettNr', 'SeteNr', 'VognNr', 'VognID', 'Avgangstid']
elif seteEllerSeng == 'seng':
    header = ['BillettNr', 'KupéNr', 'VognNr', 'VognID', 'Avgangstid']
print('-' * (len(header) * 15 + 1))
print('|', end='')
for h in header:
    print(f' {h:<12} |', end='')
print()
print('-' * (len(header) * 15 + 1))
for row in rows:
    print('|', end='')
    for value in row:
        print(f' {str(value):<12} |', end='')
    print()
print('-' * (len(header) * 15 + 1))
print('')

# Antall billetter bruker ønsker å kjøpe kan ikke være større enn antall ledige billetter
valid_antall = False
gyldige_billetter = True
# Antar at bruker skriver inn valid antall etter hvert, hvis ikke blir det uendelig loop
while not valid_antall: 

    # Sjekker først om bruker i det hele tatt kan kjøpe billetter
    if rows[0][0] == 0:
        valid_antall = True
        gyldige_billetter = False

    else: 
        antall = int(input('Hvor mange billetter ønsker du å kjøpe?'))
        if antall <= len(rows):
            valid_antall = True

# Henter ut nåværende dato og tidspunkt
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H:%M:%S.%f")

if not gyldige_billetter:
    print('Det var ingen ledige billetter')

elif antall == 0:
    print('Du ønsker ikke å kjøpe noen billetter')

else: 
    # Bruker skal ikke kunne kjøpe en billett den har kjøpt fra før
    nylig_kjøpte = []
    
    # Bruker skal velge hvilken hvilken billett den ønsker å kjøpe
    for i in range(1, antall+1):
        print('Nå skal du få velge billett nr. ' + str(i))
        kjøpt_samme = False

        # Får velge billett frem til den velger et gyldig billettNr
        # Antar at bruker skriver inn riktig antall etterhvert 
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