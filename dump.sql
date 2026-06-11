BEGIN TRANSACTION;
CREATE TABLE Allieva (
    ID_Allieva INT PRIMARY KEY,
    Nome VARCHAR(50) NOT NULL,
    Cognome VARCHAR(50) NOT NULL,
    Telefono VARCHAR(20) NOT NULL,
    Eta INT NOT NULL CHECK (Eta > 0)
, Certificato_Medico DATE);
INSERT INTO "Allieva" VALUES(1,'Giulia','Rossi','3331111111',12,'2026-04-09');
INSERT INTO "Allieva" VALUES(2,'Martina','Bianchi','3332222222',15,'2026-04-22');
INSERT INTO "Allieva" VALUES(3,'Sara','Verdi','3333333333',18,'2026-04-24');
INSERT INTO "Allieva" VALUES(4,'Chiara','Esposito','3334444444',14,'2026-04-09');
INSERT INTO "Allieva" VALUES(5,'Alessia','Romano','3335555555',17,NULL);
CREATE TABLE Allieve (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        data_nascita DATE,
        telefono TEXT,
        email TEXT,
        data_iscrizione DATE,
        id_corso INTEGER,
        certificato_medico DATE,
        FOREIGN KEY (id_corso) REFERENCES Corsi(id)
    );
INSERT INTO "Allieve" VALUES(1,'Giulia','Rossi','2015-05-12','3401234567','giulia@famiglia.it','2026-03-28',1,'2026-05-27');
INSERT INTO "Allieve" VALUES(2,'Sofia','Bianchi','2010-08-20','3407654321','sofia@famiglia.it','2026-03-28',2,'2026-04-30');
INSERT INTO "Allieve" VALUES(3,'Martina','Verdi','2012-03-15','3409876543','martina@famiglia.it','2026-03-28',3,'2026-05-27');
INSERT INTO "Allieve" VALUES(4,'Elena','Neri','2008-11-30','3401112223','elena@famiglia.it','2026-03-28',4,'2026-04-27');
INSERT INTO "Allieve" VALUES(5,'Chiara','Gialli','2014-01-10','3403334445','chiara@famiglia.it','2026-03-28',5,'2026-05-27');
CREATE TABLE Assegnazione_Costumi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_allieva INTEGER,
        id_costume INTEGER,
        id_coreografia INTEGER,
        pagato BOOLEAN DEFAULT 0,
        consegnato BOOLEAN DEFAULT 0,
        FOREIGN KEY (id_allieva) REFERENCES Allieve(id),
        FOREIGN KEY (id_costume) REFERENCES Costumi(id),
        FOREIGN KEY (id_coreografia) REFERENCES Coreografie(id)
    );
INSERT INTO "Assegnazione_Costumi" VALUES(1,1,1,1,1,1);
INSERT INTO "Assegnazione_Costumi" VALUES(2,2,1,1,1,0);
INSERT INTO "Assegnazione_Costumi" VALUES(3,3,2,2,0,0);
CREATE TABLE Classico (
    ID_Corso INT PRIMARY KEY,
    Repertorio VARCHAR(100) NOT NULL,
    FOREIGN KEY (ID_Corso) REFERENCES Corso(ID_Corso)
        ON DELETE CASCADE
);
INSERT INTO "Classico" VALUES(1,'Lago dei Cigni');
CREATE TABLE Competizione (
    ID_Concorso INT PRIMARY KEY,
    Classifica INT,
    Numero_Giudici INT NOT NULL CHECK (Numero_Giudici > 0)
);
INSERT INTO "Competizione" VALUES(1,1,5);
INSERT INTO "Competizione" VALUES(2,2,4);
INSERT INTO "Competizione" VALUES(3,3,6);
CREATE TABLE Contemporaneo (
    ID_Corso INT PRIMARY KEY,
    Fluidita VARCHAR(100) NOT NULL,
    FOREIGN KEY (ID_Corso) REFERENCES Corso(ID_Corso)
        ON DELETE CASCADE
);
INSERT INTO "Contemporaneo" VALUES(3,'Movimento fluido');
CREATE TABLE Coreografie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_saggio INTEGER,
        id_corso INTEGER,
        id_maestra INTEGER, atto INTEGER DEFAULT 1, ordine_uscita INTEGER, musica TEXT, durata INTEGER,
        FOREIGN KEY (id_saggio) REFERENCES Saggi(id),
        FOREIGN KEY (id_corso) REFERENCES Corsi(id),
        FOREIGN KEY (id_maestra) REFERENCES Maestre(id)
    );
INSERT INTO "Coreografie" VALUES(1,'napoli',1,5,1,3,4,'napoletane',40);
INSERT INTO "Coreografie" VALUES(2,'bridgerton',1,3,3,2,2,'violino',30);
INSERT INTO "Coreografie" VALUES(3,'Contemporary Flow',1,4,2,1,1,'mirko',5);
INSERT INTO "Coreografie" VALUES(4,'la bella addormentata',1,2,1,1,3,'la bella addormentata ',4);
CREATE TABLE Corsi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        livello TEXT,
        fascia_eta TEXT,
        id_maestra INTEGER,
        FOREIGN KEY (id_maestra) REFERENCES Maestre(id)
    );
INSERT INTO "Corsi" VALUES(1,'Propedeutica','Base','4-6 anni',1);
INSERT INTO "Corsi" VALUES(2,'Classico Avanzato','Avanzato','14-18 anni',1);
INSERT INTO "Corsi" VALUES(3,'Modern Jazz','Intermedio','10-13 anni',2);
INSERT INTO "Corsi" VALUES(4,'Contemporaneo Open','Tutti','Adulti',3);
INSERT INTO "Corsi" VALUES(5,'Urban Dance','Intermedio','12-16 anni',4);
CREATE TABLE Corso (
    ID_Corso INT PRIMARY KEY,
    Orario VARCHAR(50) NOT NULL,
    ID_Maestra INT NOT NULL,
    FOREIGN KEY (ID_Maestra) REFERENCES Maestra(ID_Maestra)
);
INSERT INTO "Corso" VALUES(1,'Lunedi 16:00',1);
INSERT INTO "Corso" VALUES(2,'Martedi 17:00',2);
INSERT INTO "Corso" VALUES(3,'Mercoledi 16:00',3);
INSERT INTO "Corso" VALUES(4,'Giovedi 18:00',4);
CREATE TABLE Costumi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descrizione TEXT,
        taglia TEXT,
        prezzo REAL,
        fornitore TEXT,
        stato_ordine TEXT DEFAULT 'In magazzino'
    );
INSERT INTO "Costumi" VALUES(1,'Tutù Bianco Classico','Tutù con corpetto decorato','S',45.0,'DanzaShop','Consegnato');
INSERT INTO "Costumi" VALUES(2,'Leggings Viola e Top','Completo moderno glitterato','M',35.0,'BalletWorld','In magazzino');
INSERT INTO "Costumi" VALUES(3,'Vestito Contemporaneo','Sottoveste in seta azzurra','M',40.0,'CustomDesign','Ordinato');
CREATE TABLE Hiphop (
    ID_Corso INT PRIMARY KEY,
    Crew VARCHAR(100) NOT NULL,
    FOREIGN KEY (ID_Corso) REFERENCES Corso(ID_Corso)
        ON DELETE CASCADE
);
INSERT INTO "Hiphop" VALUES(4,'Urban Queens');
CREATE TABLE Iscrizione_Competizione (
    ID_Allieva INT,
    ID_Concorso INT,
    PRIMARY KEY (ID_Allieva, ID_Concorso),
    FOREIGN KEY (ID_Allieva) REFERENCES Allieva(ID_Allieva)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Concorso) REFERENCES Competizione(ID_Concorso)
        ON DELETE CASCADE
);
INSERT INTO "Iscrizione_Competizione" VALUES(1,1);
INSERT INTO "Iscrizione_Competizione" VALUES(2,1);
INSERT INTO "Iscrizione_Competizione" VALUES(3,2);
INSERT INTO "Iscrizione_Competizione" VALUES(4,3);
INSERT INTO "Iscrizione_Competizione" VALUES(5,2);
CREATE TABLE Iscrizione_Corso (
    ID_Allieva INT,
    ID_Corso INT,
    PRIMARY KEY (ID_Allieva, ID_Corso),
    FOREIGN KEY (ID_Allieva) REFERENCES Allieva(ID_Allieva)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Corso) REFERENCES Corso(ID_Corso)
        ON DELETE CASCADE
);
INSERT INTO "Iscrizione_Corso" VALUES(1,1);
INSERT INTO "Iscrizione_Corso" VALUES(1,2);
INSERT INTO "Iscrizione_Corso" VALUES(2,2);
INSERT INTO "Iscrizione_Corso" VALUES(2,4);
INSERT INTO "Iscrizione_Corso" VALUES(3,3);
INSERT INTO "Iscrizione_Corso" VALUES(3,4);
INSERT INTO "Iscrizione_Corso" VALUES(4,1);
INSERT INTO "Iscrizione_Corso" VALUES(4,3);
INSERT INTO "Iscrizione_Corso" VALUES(5,2);
INSERT INTO "Iscrizione_Corso" VALUES(5,4);
CREATE TABLE Lezioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        giorno_settimana TEXT NOT NULL,
        ora_inizio TEXT NOT NULL,
        ora_fine TEXT NOT NULL,
        sala TEXT,
        id_corso INTEGER,
        id_maestra INTEGER,
        FOREIGN KEY (id_corso) REFERENCES Corsi(id),
        FOREIGN KEY (id_maestra) REFERENCES Maestre(id)
    );
INSERT INTO "Lezioni" VALUES(1,'Lunedì','16:00','17:00','Sala A',1,1);
INSERT INTO "Lezioni" VALUES(2,'Lunedì','17:00','19:00','Sala A',2,1);
INSERT INTO "Lezioni" VALUES(3,'Martedì','16:30','18:00','Sala B',3,2);
INSERT INTO "Lezioni" VALUES(4,'Mercoledì','18:00','19:30','Sala A',4,3);
INSERT INTO "Lezioni" VALUES(5,'Giovedì','16:00','17:00','Sala A',1,1);
INSERT INTO "Lezioni" VALUES(6,'Venerdì','17:00','18:30','Sala C',5,4);
CREATE TABLE Maestra (
    ID_Maestra INT PRIMARY KEY,
    Nome VARCHAR(50) NOT NULL,
    Cognome VARCHAR(50) NOT NULL,
    Telefono VARCHAR(20) NOT NULL
);
INSERT INTO "Maestra" VALUES(1,'Elena','Moretti','3201111111');
INSERT INTO "Maestra" VALUES(2,'Laura','Conti','3202222222');
INSERT INTO "Maestra" VALUES(3,'Francesca','Ricci','3203333333');
INSERT INTO "Maestra" VALUES(4,'Valentina','Greco','3204444444');
CREATE TABLE Maestre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        telefono TEXT,
        email TEXT,
        specializzazione TEXT,
        compenso_mensile REAL
    );
INSERT INTO "Maestre" VALUES(1,'Alessandra','Celentano','3331234567','alessandra@danza.it','Classico',1500.0);
INSERT INTO "Maestre" VALUES(2,'Kledi','Kadiu','3337654321','kledi@danza.it','Moderno',1300.0);
INSERT INTO "Maestre" VALUES(3,'Veronica','Peparini','3339876543','veronica@danza.it','Contemporaneo',1400.0);
INSERT INTO "Maestre" VALUES(4,'Garrison','Rochelle','3331112223','garrison@danza.it','Hip Hop',1200.0);
CREATE TABLE Moderno (
    ID_Corso INT PRIMARY KEY,
    Espressione VARCHAR(100) NOT NULL,
    FOREIGN KEY (ID_Corso) REFERENCES Corso(ID_Corso)
        ON DELETE CASCADE
);
INSERT INTO "Moderno" VALUES(2,'Espressivita corporea');
CREATE TABLE Pagamenti_Allieve (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_allieva INTEGER,
        importo REAL NOT NULL,
        data_scadenza DATE NOT NULL,
        data_pagamento DATE,
        stato TEXT DEFAULT 'Da pagare',
        descrizione TEXT,
        FOREIGN KEY (id_allieva) REFERENCES Allieve(id)
    );
INSERT INTO "Pagamenti_Allieve" VALUES(1,1,50.0,'2026-04-27','2026-04-27','Pagato','Mensilità Aprile');
INSERT INTO "Pagamenti_Allieve" VALUES(2,2,60.0,'2026-03-28','2026-04-30','Pagato','Mensilità Marzo');
INSERT INTO "Pagamenti_Allieve" VALUES(3,3,55.0,'2026-05-27',NULL,'Da pagare','Mensilità Maggio');
INSERT INTO "Pagamenti_Allieve" VALUES(4,4,70.0,'2026-04-27','2026-04-27','Pagato','Mensilità Aprile');
INSERT INTO "Pagamenti_Allieve" VALUES(5,5,50.0,'2026-04-27','2026-04-27','Pagato','Iscrizione Annuale');
CREATE TABLE Pagamenti_Maestre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_maestra INTEGER,
        importo REAL NOT NULL,
        data_scadenza DATE NOT NULL,
        data_pagamento DATE,
        stato TEXT DEFAULT 'Da pagare',
        descrizione TEXT,
        FOREIGN KEY (id_maestra) REFERENCES Maestre(id)
    );
INSERT INTO "Pagamenti_Maestre" VALUES(1,1,1500.0,'2026-04-27','2026-04-27','Pagato','Stipendio Aprile');
INSERT INTO "Pagamenti_Maestre" VALUES(2,2,1300.0,'2026-03-28','2026-03-28','Pagato','Stipendio Marzo');
INSERT INTO "Pagamenti_Maestre" VALUES(3,3,1400.0,'2026-04-27',NULL,'Da pagare','Stipendio Aprile');
CREATE TABLE Saggi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titolo TEXT NOT NULL,
        data DATE,
        luogo TEXT,
        descrizione TEXT
    , ora_inizio TEXT, stato TEXT DEFAULT 'In preparazione', numero_atti INTEGER DEFAULT 1, durata_totale INTEGER DEFAULT 0);
INSERT INTO "Saggi" VALUES(1,'Saggio di fine anno 2025/2026','2026-05-11','Teatro Lendi',NULL,'19:00','In preparazione',3,240);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('Maestre',4);
INSERT INTO "sqlite_sequence" VALUES('Corsi',5);
INSERT INTO "sqlite_sequence" VALUES('Allieve',5);
INSERT INTO "sqlite_sequence" VALUES('Lezioni',6);
INSERT INTO "sqlite_sequence" VALUES('Pagamenti_Allieve',5);
INSERT INTO "sqlite_sequence" VALUES('Pagamenti_Maestre',3);
INSERT INTO "sqlite_sequence" VALUES('Coreografie',4);
INSERT INTO "sqlite_sequence" VALUES('Costumi',3);
INSERT INTO "sqlite_sequence" VALUES('Assegnazione_Costumi',3);
INSERT INTO "sqlite_sequence" VALUES('Saggi',1);
COMMIT;
