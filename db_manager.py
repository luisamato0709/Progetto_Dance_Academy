import sqlite3
import os
from datetime import datetime, date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'Scuola.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop existing tables to start fresh as requested
    tables = [
        'Assegnazione_Costumi', 'Costumi', 'Coreografie', 'Saggi', 
        'Pagamenti_Maestre', 'Pagamenti_Allieve', 'Lezioni', 'Corsi', 
        'Maestre', 'Allieve'
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # Create Tables
    cursor.execute('''
    CREATE TABLE Maestre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        telefono TEXT,
        email TEXT,
        specializzazione TEXT,
        compenso_mensile REAL
    )''')

    cursor.execute('''
    CREATE TABLE Corsi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        livello TEXT,
        fascia_eta TEXT,
        id_maestra INTEGER,
        FOREIGN KEY (id_maestra) REFERENCES Maestre(id)
    )''')

    cursor.execute('''
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
    )''')

    cursor.execute('''
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
    )''')

    cursor.execute('''
    CREATE TABLE Pagamenti_Allieve (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_allieva INTEGER,
        importo REAL NOT NULL,
        data_scadenza DATE NOT NULL,
        data_pagamento DATE,
        stato TEXT DEFAULT 'Da pagare',
        descrizione TEXT,
        FOREIGN KEY (id_allieva) REFERENCES Allieve(id)
    )''')

    cursor.execute('''
    CREATE TABLE Pagamenti_Maestre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_maestra INTEGER,
        importo REAL NOT NULL,
        data_scadenza DATE NOT NULL,
        data_pagamento DATE,
        stato TEXT DEFAULT 'Da pagare',
        descrizione TEXT,
        FOREIGN KEY (id_maestra) REFERENCES Maestre(id)
    )''')

    cursor.execute('''
    CREATE TABLE Saggi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titolo TEXT NOT NULL,
        data DATE,
        luogo TEXT,
        ora_inizio TEXT,
        stato TEXT DEFAULT 'In preparazione',
        numero_atti INTEGER DEFAULT 1,
        durata_totale INTEGER DEFAULT 0
    )''')

    cursor.execute('''
    CREATE TABLE Coreografie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_saggio INTEGER,
        id_corso INTEGER,
        id_maestra INTEGER,
        atto INTEGER DEFAULT 1,
        ordine_uscita INTEGER,
        musica TEXT,
        durata INTEGER,
        FOREIGN KEY (id_saggio) REFERENCES Saggi(id),
        FOREIGN KEY (id_corso) REFERENCES Corsi(id),
        FOREIGN KEY (id_maestra) REFERENCES Maestre(id)
    )''')

    cursor.execute('''
    CREATE TABLE Costumi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descrizione TEXT,
        taglia TEXT,
        prezzo REAL,
        fornitore TEXT,
        stato_ordine TEXT DEFAULT 'In magazzino'
    )''')

    cursor.execute('''
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
    )''')

    # Sample Data
    maestre_data = [
        ('Alessandra', 'Celentano', '3331234567', 'alessandra@danza.it', 'Classico', 1500.0),
        ('Kledi', 'Kadiu', '3337654321', 'kledi@danza.it', 'Moderno', 1300.0),
        ('Veronica', 'Peparini', '3339876543', 'veronica@danza.it', 'Contemporaneo', 1400.0),
        ('Garrison', 'Rochelle', '3331112223', 'garrison@danza.it', 'Hip Hop', 1200.0)
    ]
    cursor.executemany('INSERT INTO Maestre (nome, cognome, telefono, email, specializzazione, compenso_mensile) VALUES (?,?,?,?,?,?)', maestre_data)

    corsi_data = [
        ('Propedeutica', 'Base', '4-6 anni', 1),
        ('Classico Avanzato', 'Avanzato', '14-18 anni', 1),
        ('Modern Jazz', 'Intermedio', '10-13 anni', 2),
        ('Contemporaneo Open', 'Tutti', 'Adulti', 3),
        ('Urban Dance', 'Intermedio', '12-16 anni', 4)
    ]
    cursor.executemany('INSERT INTO Corsi (nome, livello, fascia_eta, id_maestra) VALUES (?,?,?,?)', corsi_data)

    today = date.today().isoformat()
    last_month = (date.today() - timedelta(days=30)).isoformat()
    next_month = (date.today() + timedelta(days=30)).isoformat()

    allieve_data = [
        ('Giulia', 'Rossi', '2015-05-12', '3401234567', 'giulia@famiglia.it', last_month, 1, next_month),
        ('Sofia', 'Bianchi', '2010-08-20', '3407654321', 'sofia@famiglia.it', last_month, 2, last_month),
        ('Martina', 'Verdi', '2012-03-15', '3409876543', 'martina@famiglia.it', last_month, 3, next_month),
        ('Elena', 'Neri', '2008-11-30', '3401112223', 'elena@famiglia.it', last_month, 4, None),
        ('Chiara', 'Gialli', '2014-01-10', '3403334445', 'chiara@famiglia.it', last_month, 5, next_month)
    ]
    cursor.executemany('INSERT INTO Allieve (nome, cognome, data_nascita, telefono, email, data_iscrizione, id_corso, certificato_medico) VALUES (?,?,?,?,?,?,?,?)', allieve_data)

    lezioni_data = [
        ('Lunedì', '16:00', '17:00', 'Sala A', 1, 1),
        ('Lunedì', '17:00', '19:00', 'Sala A', 2, 1),
        ('Martedì', '16:30', '18:00', 'Sala B', 3, 2),
        ('Mercoledì', '18:00', '19:30', 'Sala A', 4, 3),
        ('Giovedì', '16:00', '17:00', 'Sala A', 1, 1),
        ('Venerdì', '17:00', '18:30', 'Sala C', 5, 4)
    ]
    cursor.executemany('INSERT INTO Lezioni (giorno_settimana, ora_inizio, ora_fine, sala, id_corso, id_maestra) VALUES (?,?,?,?,?,?)', lezioni_data)

    # Payments
    pagamenti_allieve = [
        (1, 50.0, today, today, 'Pagato', 'Mensilità Aprile'),
        (2, 60.0, last_month, None, 'In ritardo', 'Mensilità Marzo'),
        (3, 55.0, next_month, None, 'Da pagare', 'Mensilità Maggio'),
        (4, 70.0, today, None, 'Da pagare', 'Mensilità Aprile'),
        (5, 50.0, today, today, 'Pagato', 'Iscrizione Annuale')
    ]
    cursor.executemany('INSERT INTO Pagamenti_Allieve (id_allieva, importo, data_scadenza, data_pagamento, stato, descrizione) VALUES (?,?,?,?,?,?)', pagamenti_allieve)

    pagamenti_maestre = [
        (1, 1500.0, today, None, 'Da pagare', 'Stipendio Aprile'),
        (2, 1300.0, last_month, last_month, 'Pagato', 'Stipendio Marzo'),
        (3, 1400.0, today, None, 'Da pagare', 'Stipendio Aprile')
    ]
    cursor.executemany('INSERT INTO Pagamenti_Maestre (id_maestra, importo, data_scadenza, data_pagamento, stato, descrizione) VALUES (?,?,?,?,?,?)', pagamenti_maestre)

    # Saggio and Coreografie
    
    coreografie_data = [
        ('Il Lago dei Cigni (Estratti)', 1, 2, 1),
        ('Modern Vibes', 1, 3, 2),
        ('Contemporary Flow', 1, 4, 3)
    ]
    cursor.executemany('INSERT INTO Coreografie (nome, id_saggio, id_corso, id_maestra) VALUES (?,?,?,?)', coreografie_data)

    # Costumi
    costumi_data = [
        ('Tutù Bianco Classico', 'Tutù con corpetto decorato', 'S', 45.0, 'DanzaShop', 'Consegnato'),
        ('Leggings Viola e Top', 'Completo moderno glitterato', 'M', 35.0, 'BalletWorld', 'In magazzino'),
        ('Vestito Contemporaneo', 'Sottoveste in seta azzurra', 'M', 40.0, 'CustomDesign', 'Ordinato')
    ]
    cursor.executemany('INSERT INTO Costumi (nome, descrizione, taglia, prezzo, fornitore, stato_ordine) VALUES (?,?,?,?,?,?)', costumi_data)

    assegnazioni = [
        (1, 1, 1, 1, 1), # Giulia, Tutù, Lago dei cigni, pagato, consegnato
        (2, 1, 1, 1, 0), # Sofia, Tutù, Lago dei cigni, pagato, non consegnato
        (3, 2, 2, 0, 0)  # Martina, Leggings, Modern Vibes, non pagato, non consegnato
    ]
    cursor.executemany('INSERT INTO Assegnazione_Costumi (id_allieva, id_costume, id_coreografia, pagato, consegnato) VALUES (?,?,?,?,?)', assegnazioni)

    conn.commit()
    conn.close()

def get_stats():
    conn = get_db_connection()
    stats = {}
    stats['allieve'] = conn.execute('SELECT COUNT(*) FROM Allieve').fetchone()[0]
    stats['maestre'] = conn.execute('SELECT COUNT(*) FROM Maestre').fetchone()[0]
    stats['corsi'] = conn.execute('SELECT COUNT(*) FROM Corsi').fetchone()[0]
    
    # Pagamenti in scadenza (prossimi 7 giorni o scaduti non pagati)
    query_p_allieve = "SELECT COUNT(*) FROM Pagamenti_Allieve WHERE stato != 'Pagato' AND data_scadenza <= date('now', '+7 days')"
    stats['pagamenti_allieve_scadenza'] = conn.execute(query_p_allieve).fetchone()[0]
    
    query_p_maestre = "SELECT COUNT(*) FROM Pagamenti_Maestre WHERE stato != 'Pagato' AND data_scadenza <= date('now', '+7 days')"
    stats['pagamenti_maestre_scadenza'] = conn.execute(query_p_maestre).fetchone()[0]

    # Lezioni di oggi
    giorni = {0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'}
    oggi_sett = giorni[date.today().weekday()]
    stats['lezioni_oggi'] = conn.execute('SELECT COUNT(*) FROM Lezioni WHERE giorno_settimana = ?', (oggi_sett,)).fetchone()[0]

    # Costumi non consegnati
    stats['costumi_non_consegnati'] = conn.execute('SELECT COUNT(*) FROM Assegnazione_Costumi WHERE consegnato = 0').fetchone()[0]

    # Stato saggio (titolo del prossimo saggio)
    prossimo_saggio = conn.execute('SELECT titolo FROM Saggi ORDER BY data ASC LIMIT 1').fetchone()
    stats['stato_saggio'] = prossimo_saggio['titolo'] if prossimo_saggio else 'Nessuno'

    conn.close()
    return stats

def get_allieve():
    conn = get_db_connection()
    query = '''
        SELECT a.*, c.nome as nome_corso 
        FROM Allieve a 
        LEFT JOIN Corsi c ON a.id_corso = c.id 
        ORDER BY a.cognome, a.nome
    '''
    allieve = conn.execute(query).fetchall()
    conn.close()
    return allieve

def get_maestre():
    conn = get_db_connection()
    maestre = conn.execute('SELECT * FROM Maestre ORDER BY cognome, nome').fetchall()
    conn.close()
    return maestre

def get_corsi():
    conn = get_db_connection()
    query = '''
        SELECT c.*, m.nome as nome_maestra, m.cognome as cognome_maestra 
        FROM Corsi c 
        JOIN Maestre m ON c.id_maestra = m.id 
        ORDER BY c.nome
    '''
    corsi = conn.execute(query).fetchall()
    conn.close()
    return corsi

def get_calendario():
    conn = get_db_connection()
    query = '''
        SELECT l.*, c.nome as nome_corso, m.nome as nome_maestra, m.cognome as cognome_maestra
        FROM Lezioni l
        JOIN Corsi c ON l.id_corso = c.id
        JOIN Maestre m ON l.id_maestra = m.id
        ORDER BY 
            CASE giorno_settimana 
                WHEN 'Lunedì' THEN 1 
                WHEN 'Martedì' THEN 2 
                WHEN 'Mercoledì' THEN 3 
                WHEN 'Giovedì' THEN 4 
                WHEN 'Venerdì' THEN 5 
                WHEN 'Sabato' THEN 6 
                WHEN 'Domenica' THEN 7 
            END, ora_inizio
    '''
    lezioni = conn.execute(query).fetchall()
    conn.close()
    
    # Raggruppa per giorno
    calendario = {}
    for l in lezioni:
        giorno = l['giorno_settimana']
        if giorno not in calendario:
            calendario[giorno] = []
        calendario[giorno].append(l)
    return calendario

def get_lezioni_oggi_completo():
    conn = get_db_connection()
    giorni = {0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'}
    oggi_sett = giorni[date.today().weekday()]
    query = '''
        SELECT l.*, c.nome as nome_corso, m.nome as nome_maestra, m.cognome as cognome_maestra,
               (SELECT COUNT(*) FROM Allieve WHERE id_corso = l.id_corso) as num_allieve
        FROM Lezioni l
        JOIN Corsi c ON l.id_corso = c.id
        JOIN Maestre m ON l.id_maestra = m.id
        WHERE l.giorno_settimana = ?
        ORDER BY l.ora_inizio
    '''
    lezioni = conn.execute(query, (oggi_sett,)).fetchall()
    conn.close()
    return lezioni

def get_prossime_scadenze(limit=5):
    conn = get_db_connection()
    query = '''
        SELECT 'Allieva' as tipo, a.nome, a.cognome, p.importo, p.data_scadenza
        FROM Pagamenti_Allieve p
        JOIN Allieve a ON p.id_allieva = a.id
        WHERE p.stato != 'Pagato'
        UNION ALL
        SELECT 'Maestra' as tipo, m.nome, m.cognome, p.importo, p.data_scadenza
        FROM Pagamenti_Maestre p
        JOIN Maestre m ON p.id_maestra = m.id
        WHERE p.stato != 'Pagato'
        ORDER BY data_scadenza ASC
        LIMIT ?
    '''
    scadenze = conn.execute(query, (limit,)).fetchall()
    conn.close()
    return scadenze

def get_pagamenti_allieve():
    conn = get_db_connection()
    query = '''
        SELECT p.*, a.nome as nome_allieva, a.cognome as cognome_allieva
        FROM Pagamenti_Allieve p
        JOIN Allieve a ON p.id_allieva = a.id
        ORDER BY p.data_scadenza DESC
    '''
    pagamenti = conn.execute(query).fetchall()
    conn.close()
    return pagamenti

def get_pagamenti_maestre():
    conn = get_db_connection()
    query = '''
        SELECT p.*, m.nome as nome_maestra, m.cognome as cognome_maestra
        FROM Pagamenti_Maestre p
        JOIN Maestre m ON p.id_maestra = m.id
        ORDER BY p.data_scadenza DESC
    '''
    pagamenti = conn.execute(query).fetchall()
    conn.close()
    return pagamenti

def set_pagamento_allieva(id_pagamento):
    conn = get_db_connection()
    conn.execute('UPDATE Pagamenti_Allieve SET stato = "Pagato", data_pagamento = ? WHERE id = ?', (date.today().isoformat(), id_pagamento))
    conn.commit()
    conn.close()

def set_pagamento_maestra(id_pagamento):
    conn = get_db_connection()
    conn.execute('UPDATE Pagamenti_Maestre SET stato = "Pagato", data_pagamento = ? WHERE id = ?', (date.today().isoformat(), id_pagamento))
    conn.commit()
    conn.close()

def get_saggi_completo():
    conn = get_db_connection()
    saggi = conn.execute('SELECT * FROM Saggi').fetchall()
    saggi_list = []
    for s in saggi:
        s_dict = dict(s)
        # Coreografie
        query_coreo = '''
            SELECT cor.*, c.nome as nome_corso, m.nome as nome_maestra, m.cognome as cognome_maestra,
                   (SELECT COUNT(*) FROM Allieve WHERE id_corso = cor.id_corso) as num_allieve
            FROM Coreografie cor
            JOIN Corsi c ON cor.id_corso = c.id
            JOIN Maestre m ON cor.id_maestra = m.id
            WHERE cor.id_saggio = ?
            ORDER BY cor.atto, cor.ordine_uscita
        '''
        coreografie = conn.execute(query_coreo, (s['id'],)).fetchall()
        
        # Raggruppa per atto
        atti = {}
        for c in coreografie:
            atto_num = c['atto']
            if atto_num not in atti:
                atti[atto_num] = []
            atti[atto_num].append(c)
        
        s_dict['atti'] = atti
        saggi_list.append(s_dict)
    conn.close()
    return saggi_list

def get_costumi_completo():
    conn = get_db_connection()
    query = '''
        SELECT ac.*, c.nome as nome_costume, c.taglia, c.prezzo, 
               a.nome as nome_allieva, a.cognome as cognome_allieva,
               cor.nome as nome_coreografia
        FROM Assegnazione_Costumi ac
        JOIN Costumi c ON ac.id_costume = c.id
        JOIN Allieve a ON ac.id_allieva = a.id
        JOIN Coreografie cor ON ac.id_coreografia = cor.id
    '''
    costumi = conn.execute(query).fetchall()
    conn.close()
    return costumi

def get_allieva_details(id_allieva):
    conn = get_db_connection()
    allieva = conn.execute('SELECT a.*, c.nome as nome_corso FROM Allieve a LEFT JOIN Corsi c ON a.id_corso = c.id WHERE a.id = ?', (id_allieva,)).fetchone()
    if not allieva:
        conn.close()
        return None
    
    pagamenti = conn.execute('SELECT * FROM Pagamenti_Allieve WHERE id_allieva = ? ORDER BY data_scadenza DESC', (id_allieva,)).fetchall()
    costumi = conn.execute('''
        SELECT ac.*, c.nome as nome_costume, cor.nome as nome_coreografia
        FROM Assegnazione_Costumi ac
        JOIN Costumi c ON ac.id_costume = c.id
        JOIN Coreografie cor ON ac.id_coreografia = cor.id
        WHERE ac.id_allieva = ?
    ''', (id_allieva,)).fetchall()
    
    conn.close()
    return {
        'info': allieva,
        'pagamenti': pagamenti,
        'costumi': costumi
    }

def update_certificato(id_allieva, data_scadenza):
    conn = get_db_connection()
    conn.execute('UPDATE Allieve SET certificato_medico = ? WHERE id = ?', (data_scadenza, id_allieva))
    conn.commit()
    conn.close()

def get_allieve_certificati_critici():
    conn = get_db_connection()
    query = '''
        SELECT id, nome, cognome, certificato_medico
        FROM Allieve
        WHERE certificato_medico IS NULL OR certificato_medico < date('now')
        ORDER BY certificato_medico ASC, cognome ASC
    '''
    allieve = conn.execute(query).fetchall()
    conn.close()
    return allieve
def add_allieva(nome, cognome, data_nascita, telefono, email, data_iscrizione, id_corso, certificato_medico):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO Allieve (nome, cognome, data_nascita, telefono, email, data_iscrizione, id_corso, certificato_medico)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, cognome, data_nascita, telefono, email, data_iscrizione, id_corso, certificato_medico))
    conn.commit()
    conn.close()
def add_maestra(nome, cognome, telefono, email, specializzazione, compenso_mensile):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO Maestre (nome, cognome, telefono, email, specializzazione, compenso_mensile)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, cognome, telefono, email, specializzazione, compenso_mensile))
    conn.commit()
    conn.close()

def add_corso(nome, livello, fascia_eta, id_maestra):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO Corsi (nome, livello, fascia_eta, id_maestra)
        VALUES (?, ?, ?, ?)
    ''', (nome, livello, fascia_eta, id_maestra))
    conn.commit()
    conn.close()
def add_saggio(titolo, data, luogo, ora_inizio, stato, numero_atti, durata_totale):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO Saggi (titolo, data, luogo, ora_inizio, stato, numero_atti, durata_totale)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (titolo, data, luogo, ora_inizio, stato, numero_atti, durata_totale))
    conn.commit()
    conn.close()

def add_coreografia(nome, id_saggio, id_corso, id_maestra, atto, ordine_uscita, musica, durata):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO Coreografie (nome, id_saggio, id_corso, id_maestra, atto, ordine_uscita, musica, durata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, id_saggio, id_corso, id_maestra, atto, ordine_uscita, musica, durata))
    conn.commit()
    conn.close()
def get_coreografia(id_coreografia):
    conn = get_db_connection()
    query = 'SELECT * FROM Coreografie WHERE id = ?'
    coreo = conn.execute(query, (id_coreografia,)).fetchone()
    conn.close()
    return coreo

def update_coreografia(id_coreografia, nome, id_corso, id_maestra, atto, ordine_uscita, musica, durata):
    conn = get_db_connection()
    conn.execute('''
        UPDATE Coreografie 
        SET nome = ?, id_corso = ?, id_maestra = ?, atto = ?, ordine_uscita = ?, musica = ?, durata = ?
        WHERE id = ?
    ''', (nome, id_corso, id_maestra, atto, ordine_uscita, musica, durata, id_coreografia))
    conn.commit()
    conn.close()
