BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Jernbanestasjon" (
	"Navn"	TEXT NOT NULL UNIQUE,
	"Moh."	INTEGER NOT NULL,
	PRIMARY KEY("Navn")
);
CREATE TABLE IF NOT EXISTS "Operatør" (
	"Navn" TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Navn")
);
CREATE TABLE IF NOT EXISTS "Vognoppsett" (
	"OppsettID" INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("OppsettID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Banestrekning" (
    "Navn"	TEXT NOT NULL UNIQUE,
    "Fremdriftsenergi"	TEXT NOT NULL,
    "Hovedretning" TEXT NOT NULL,
	"StartstasjonNavn" TEXT NOT NULL,
	"EndestasjonNavn"  TEXT NOT NULL,
    CONSTRAINT "CheckFremdriftsenergi" CHECK("Fremdriftsenergi" = 'Diesel' OR "Fremdriftsenergi" = 'Elektrisk'),
	-- Antar at navn for de to strekningene 
	-- er Retning 1 og Retning 2
    CONSTRAINT "CheckHovedretning" CHECK("Hovedretning" = 'Retning1' OR "Hovedretning" = 'Retning2'),
    FOREIGN KEY("StartstasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY("EndestasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY("Navn")
);

CREATE TABLE IF NOT EXISTS "Togrute" (
	"RuteNr" INTEGER NOT NULL UNIQUE,
	"Retning" TEXT NOT NULL,
	"OperatørNavn" TEXT NOT NULL,
	"OppsettID" INTEGER NOT NULL,
	"BanestrekningNavn" TEXT NOT NULL
	CONSTRAINT "CheckRetning" CHECK("Retning" = 'MedHovedretning' OR "Retning" = 'MotHovedretning'),
	FOREIGN KEY("OperatørNavn") REFERENCES "Operatør"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("OppsettID") REFERENCES "Vognoppsett"("OppsettID") ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY("BanestrekningNavn") REFERENCES "Banestrekning"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("RuteNr")
);


CREATE TABLE IF NOT EXISTS "Dag"(
	--Ny database Dag og realsjon Kjører
	"Dag" TEXT  NOT NULL UNIQUE,
	PRIMARY KEY("Dag")
);

CREATE TABLE IF NOT EXISTS "Kjører"(
	"Dag" TEXT NOT NULL,
	"RuteNr" INTEGER NOT NULL,
	FOREIGN KEY("RuteNr") REFERENCES "Togrute"("RuteNr") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Dag") REFERENCES "Dag"("Dag") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Dag", "RuteNr")
);


CREATE TABLE IF NOT EXISTS "Vogntype" (
	-- VognID tekst og ikke tall fordi det er det unike navnet
	"VognID" TEXT NOT NULL UNIQUE,
	"Tilgjengelighet" BOOLEAN NOT NULL,
	PRIMARY KEY("VognID")
);
CREATE TABLE IF NOT EXISTS "Sittevogn" (
	"AntallSeter" INTEGER NOT NULL,
	"VognID" TEXT NOT NULL,
	"Tilgjengelighet" BOOLEAN NOT NULL,
	"OperatørNavn" TEXT NOT NULL,
    CONSTRAINT "CheckAntallSeter" CHECK ("AntallSeter" > 0),
	FOREIGN KEY("VognID") REFERENCES "Vogntype"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Tilgjengelighet") REFERENCES "Vogntype"("Tilgjengelighet") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("OperatørNavn") REFERENCES "Operatør"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("VognID")
);
CREATE TABLE IF NOT EXISTS "Sovevogn" (
	"AntallSovekupeer" INTEGER NOT NULL,
	"VognID" TEXT NOT NULL,
	"Tilgjengelighet" BOOLEAN,
	"OperatørNavn" TEXT NOT NULL,
    CONSTRAINT "CheckAntallSovekupeer" CHECK ("AntallSovekupeer" > 0),
	FOREIGN KEY("VognID") REFERENCES "Vogntype"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Tilgjengelighet") REFERENCES "Vogntype"("Tilgjengelighet") ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY("OperatørNavn") REFERENCES "Operatør"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("VognID")
);
CREATE TABLE IF NOT EXISTS "Sete" (
	"SeteNr" INTEGER NOT NULL,
	"Tilgjengelighet" BOOLEAN NOT NULL,
	"VognID" TEXT NOT NULL,
    FOREIGN KEY ("VognID") REFERENCES "Sittevogn"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("SeteNr", "VognID")
);
CREATE TABLE IF NOT EXISTS "Sovekupé" (
    "KupéNr" INTEGER NOT NULL,
	"Tilgjengelighet" BOOLEAN NOT NULL,
	"VognID" TEXT NOT NULL,
	FOREIGN KEY ("VognID") REFERENCES "Sovevogn"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("KupéNr", "VognID")
);
CREATE TABLE IF NOT EXISTS "Togruteforekomst" (
	"Dato" DATE NOT NULL,
	"RuteNr" INTEGER NOT NULL,
	FOREIGN KEY("RuteNr") REFERENCES "Togrute"("RuteNr") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Dato", "RuteNr")
);
CREATE TABLE IF NOT EXISTS "Kunde" (
	"KundeNr" INTEGER NOT NULL UNIQUE,
	"Navn" TEXT NOT NULL,
	"Epost" TEXT NOT NULL,
    "MobilNr" TEXT NOT NULL,
    CONSTRAINT "CheckEpost" CHECK ("Epost" LIKE '%_@__%.__%'),
    CONSTRAINT "CheckMobilNr" CHECK ("MobilNr" LIKE '^[[:digit:]]{8}$'),
	PRIMARY KEY("KundeNr" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Kundeordre" (
	"OrdreNr" INTEGER NOT NULL UNIQUE,
	"DagKjøpt" DATE NOT NULL,
	"TidKjøpt" TIME NOT NULL,
	"Antall" INTEGER NOT NULL,
	"KundeNr" INTEGER NOT NULL,
	"RuteNr" INTEGER NOT NULL,
	"Dato" DATE NOT NULL,
	CONSTRAINT "Antall" CHECK ("Antall" > 0),
	FOREIGN KEY("KundeNr") REFERENCES "Kunde"("KundeNr") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("RuteNr") REFERENCES "Togrute"("RuteNr") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Dato") REFERENCES "Togruteforekomst"("Dato") ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY("OrdreNr" AUTOINCREMENT)
);

CREATE TABLE "Delstrekning" (
	-- Navn til delstrekning skal være gitt av de to jernbanestasjonene 
	-- (minst to bokstavers navn) med en bindestrek mellom
	"Navn"	TEXT NOT NULL UNIQUE,
	"Lengde"	INTEGER NOT NULL,
	"TypeSpor"	TEXT NOT NULL,
	"FraStasjonNavn"	TEXT NOT NULL,
	"TilStasjonNavn"	TEXT NOT NULL,
	"BanestrekningNavn"	TEXT,
	FOREIGN KEY("TilStasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("FraStasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("BanestrekningNavn") REFERENCES "Banestrekning"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Navn"),
	CONSTRAINT "TypeSpor" CHECK("TypeSpor" = 'Enkeltspor' OR "TypeSpor" = 'Dobbeltspor'),
	CONSTRAINT "CheckLengde" CHECK("Lengde" > 0),
	CONSTRAINT "Navn" CHECK("Navn" LIKE '_%-%_')
);

CREATE TABLE IF NOT EXISTS "KjøpAvSete" (
	"OrdreNr" INTEGER NOT NULL,
	"SeteNr" INTEGER NOT NULL,
	"VognID" TEXT NOT NULL,
	FOREIGN KEY("OrdreNr") REFERENCES "KundeOrdre"("OrdreNr") ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY("SeteNr", "VognID") REFERENCES "Sete"("SeteNr", "VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("OrdreNr", "SeteNr")
);
CREATE TABLE IF NOT EXISTS "KjøpAvKupé" (
	"OrdreNr" INTEGER NOT NULL,
	"KupéNr" INTEGER NOT NULL,
	"VognID" TEXT NOT NULL,
	FOREIGN KEY("OrdreNr") REFERENCES "KundeOrdre"("OrdreNr") ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY("KupéNr", "VognID") REFERENCES "SoveKupé"("KupéNr", "VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("OrdreNr", "KupéNr")
);
CREATE TABLE IF NOT EXISTS "MellomstasjonRute" (
    "Ankomsttid" TIME NOT NULL,
    "Avgangstid" TIME NOT NULL,
	"RuteNr" INTEGER NOT NULL,
	"StasjonNavn" TEXT NOT NULL,
	FOREIGN KEY("RuteNr") REFERENCES "Togrute"("RuteNr") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("RuteNr", "StasjonNavn")
);
CREATE TABLE IF NOT EXISTS "StasjonITabell" (
	"Avgangstid" TIME,
	"Ankomsttid" TIME,
	"StasjonNavn" TEXT NOT NULL,
	"TabellNr" INTEGER NOT NULL,
	FOREIGN KEY("StasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("TabellNr") REFERENCES "Togruteforekomst"("TabellNr") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("StasjonNavn", "TabellNr")
);
CREATE TABLE IF NOT EXISTS "EndestasjonRute" (
	"Ankomsttid" TIME NOT NULL,
	"StasjonNavn" TEXT NOT NULL,
	"RuteNr" INTEGER NOT NULL,
	FOREIGN KEY("RuteNr") REFERENCES "Togrute"("RuteNr") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("RuteNr", "StasjonNavn")
);
CREATE TABLE IF NOT EXISTS "StartstasjonRute" (
	"Avgangstid" TIME NOT NULL,
	"StasjonNavn" TEXT NOT NULL,
	"RuteNr" INTEGER NOT NULL,
	FOREIGN KEY("RuteNr") REFERENCES "Togrute"("RuteNr") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("RuteNr", "StasjonNavn")
);
CREATE TABLE IF NOT EXISTS "Togrutetabell" (
	"TabellNr" INTEGER UNIQUE NOT NULL,
	"RuteNr" INTEGER NOT NULL,
	FOREIGN KEY("RuteNr") REFERENCES "Togrute"("RuteNr") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("TabellNr", "RuteNr")
);
CREATE TABLE IF NOT EXISTS "VognIOppsett" (
	"VognNr" INTEGER NOT NULL,
	"VognID" TEXT NOT NULL,
	"OppsettID" INTEGER NOT NULL,
	FOREIGN KEY("VognID") REFERENCES "Vogntype"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("OppsettID") REFERENCES "Vognoppsett"("OppsettID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("VognID")
);
CREATE TABLE IF NOT EXISTS "MellomstasjonBane" (
	"BanestrekningNavn" TEXT NOT NULL,
	"StasjonNavn" TEXT NOT NULL,
	FOREIGN KEY("BanestrekningNavn") REFERENCES "Banestrekning"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StasjonNavn") REFERENCES "Jernbanestasjon"("Navn") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("BanestrekningNavn", "StasjonNavn")
);
COMMIT;