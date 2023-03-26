import sqlite3

con = sqlite3.connect("jernbaneDBdenne.db") # Må hente databasefilen
cursor = con.cursor()

startstasjon = input('Startstasjon: ')
endestasjon = input('Endestasjon: ')
date = input('Dato (YYYY-MM-DD): ')

# Sjekker format på dato
while not all(part.isdigit() for part in date.split('-')):
    print("Invalid date format")
    date = input('Dato (YYYY-MM-DD): ')
  
time = input('Tid (hh:mm:ss): ')

time_incorrect = True

# Sjekker format på tid
while time_incorrect:
    for char in time:
        if not char.isdigit() and char not in ['.', ':']:
            print("Invalid time format")
            time = input('Tid: ')
            break
    time_incorrect = False

# Finner dato til neste dag
year, month, day = map(int, date.split('-'))
if day == 31 and month == 12:
    next_day, next_month, next_year = 1, 1, year + 1
elif day == 31:
    next_day, next_month, next_year = 1, month + 1, year
else:
    next_day, next_month, next_year = day + 1, month, year
new_date = f"{next_year:04d}-{next_month:02d}-{next_day:02d}"

# Parametre som skal brukes i spørringen
params = (date, startstasjon, endestasjon, time, # Startstasjon --> endestasjon, samme dag, fra tid
          date, startstasjon, endestasjon, time, # Startstasjon --> mellomstasjon, samme dag, fra tid
          date, startstasjon, endestasjon, time, # Mellomstasjon --> endestasjon, samme dag, fra tid
          date, startstasjon, endestasjon, time, # Mellomstasjon --> mellomstasjon, samme dag, fra tid
          new_date, startstasjon, endestasjon, # Startstasjon --> endestasjon, neste dag
          new_date, startstasjon, endestasjon, # Startstasjon --> mellomstasjon, neste dag
          new_date, startstasjon, endestasjon, # Mellomstasjon --> endestasjon, neste dag
          new_date, startstasjon, endestasjon) # Mellomstasjon --> mellomstasjon, neste dag

# Spørring for togrutene
query = '''SELECT DISTINCT TR.RuteNr, TRF.Dato, SR.Avgangstid
FROM Jernbanestasjon AS JS
INNER JOIN StartstasjonRute AS SR ON (JS.Navn = SR.StasjonNavn)
INNER JOIN Togrute AS TR ON (SR.RuteNr = TR.RuteNr) 
INNER JOIN EndestasjonRute AS ER ON (ER.RuteNr = TR.RuteNr) 
INNER JOIN Togruteforekomst AS TRF ON (TRF.RuteNr = TR.RuteNr)
WHERE TRF.Dato = ? AND SR.StasjonNavn = ? AND ER.StasjonNavn = ? AND TIME(SR.Avgangstid) > ?

UNION ALL

SELECT DISTINCT TR.RuteNr, TRF.Dato, SR.Avgangstid
FROM Jernbanestasjon AS JS
INNER JOIN StartstasjonRute AS SR ON (JS.Navn = SR.StasjonNavn)
INNER JOIN Togrute AS TR ON (SR.RuteNr = TR.RuteNr)
INNER JOIN MellomstasjonRute AS MR ON (MR.RuteNr = TR.RuteNr)
INNER JOIN Togruteforekomst AS TRF ON (TRF.RuteNr = TR.RuteNr)
WHERE TRF.Dato = ? AND SR.StasjonNavn = ? AND MR.StasjonNavn = ? AND TIME(SR.Avgangstid) > ?

UNION ALL

SELECT DISTINCT TR.RuteNr, TRF.Dato, MR.Avgangstid
FROM Jernbanestasjon AS JS
INNER JOIN MellomstasjonRute AS MR ON (JS.Navn = MR.StasjonNavn)
INNER JOIN Togrute AS TR ON (MR.RuteNr = TR.RuteNr)
INNER JOIN EndestasjonRute AS ER ON (ER.RuteNr = TR.RuteNr)
INNER JOIN Togruteforekomst AS TRF ON (TRF.RuteNr = TR.RuteNr)
WHERE TRF.Dato = ? AND MR.StasjonNavn = ? AND ER.StasjonNavn = ? AND TIME(MR.Avgangstid) > ?

UNION ALL

SELECT DISTINCT TR.RuteNr, TRF.Dato, MR1.Avgangstid
FROM Jernbanestasjon AS JS
INNER JOIN MellomstasjonRute AS MR1 ON (JS.Navn = MR1.StasjonNavn)
INNER JOIN Togrute AS TR ON (MR1.RuteNr = TR.RuteNr)
INNER JOIN MellomstasjonRute AS MR2 ON (MR2.RuteNr = TR.RuteNr)
INNER JOIN Togruteforekomst AS TRF ON (TRF.RuteNr = TR.RuteNr)
WHERE TRF.Dato = ? AND MR1.StasjonNavn = ? AND MR2.StasjonNavn = ? AND TIME(MR1.Avgangstid) > ?

UNION ALL

SELECT DISTINCT TR.RuteNr, TRF.Dato, SR.Avgangstid
FROM Jernbanestasjon AS JS
INNER JOIN StartstasjonRute AS SR ON (JS.Navn = SR.StasjonNavn)
INNER JOIN Togrute AS TR ON (SR.RuteNr = TR.RuteNr)
INNER JOIN EndestasjonRute AS ER ON (ER.RuteNr = TR.RuteNr)
INNER JOIN Togruteforekomst AS TRF ON (TRF.RuteNr = TR.RuteNr)
WHERE TRF.Dato = ? AND SR.StasjonNavn = ? AND ER.StasjonNavn = ?

UNION ALL

SELECT DISTINCT TR.RuteNr, TRF.Dato, SR.Avgangstid
FROM Jernbanestasjon AS JS
INNER JOIN StartstasjonRute AS SR ON (JS.Navn = SR.StasjonNavn)
INNER JOIN Togrute AS TR ON (SR.RuteNr = TR.RuteNr)
INNER JOIN MellomstasjonRute AS MR ON (MR.RuteNr = TR.RuteNr)
INNER JOIN Togruteforekomst AS TRF ON (TRF.RuteNr = TR.RuteNr)
WHERE TRF.Dato = ? AND SR.StasjonNavn = ? AND MR.StasjonNavn = ?

UNION ALL

SELECT DISTINCT TR.RuteNr, TRF.Dato, MR.Avgangstid
FROM Jernbanestasjon AS JS
INNER JOIN MellomstasjonRute AS MR ON (JS.Navn = MR.StasjonNavn)
INNER JOIN Togrute AS TR ON (MR.RuteNr = TR.RuteNr)
INNER JOIN EndestasjonRute AS ER ON (ER.RuteNr = TR.RuteNr)
INNER JOIN Togruteforekomst AS TRF ON (TRF.RuteNr = TR.RuteNr)
WHERE TRF.Dato = ? AND MR.StasjonNavn = ? AND ER.StasjonNavn = ?

UNION ALL

SELECT DISTINCT TR.RuteNr, TRF.Dato, MR1.Avgangstid
FROM Jernbanestasjon AS JS
INNER JOIN MellomstasjonRute AS MR1 ON (JS.Navn = MR1.StasjonNavn)
INNER JOIN Togrute AS TR ON (MR1.RuteNr = TR.RuteNr)
INNER JOIN MellomstasjonRute AS MR2 ON (MR2.RuteNr = TR.RuteNr)
INNER JOIN Togruteforekomst AS TRF ON (TRF.RuteNr = TR.RuteNr)
WHERE TRF.Dato = ? AND MR1.StasjonNavn = ? AND MR2.StasjonNavn = ?'''

result = cursor.execute(query, params)
rows = result.fetchall()

# Printer pent i tabell
header = ['RuteNr', 'Dato', 'Avgangstid']
print('-' * (len(header) * 12 + 4))
print('|', end='')
for h in header:
    print(f' {h:<10} |', end='')
print()
print('-' * (len(header) * 12 + 4))
for row in rows:
    print('|', end='')
    for value in row:
        print(f' {str(value):<10} |', end='')
    print()
print('-' * (len(header) * 12 + 4))

# Close connection
con.close()