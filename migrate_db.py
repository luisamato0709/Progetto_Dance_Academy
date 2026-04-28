import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'Scuola.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Add columns to Saggi if they don't exist
    try:
        cursor.execute("ALTER TABLE Saggi ADD COLUMN ora_inizio TEXT")
    except sqlite3.OperationalError:
        pass # Already exists
        
    try:
        cursor.execute("ALTER TABLE Saggi ADD COLUMN stato TEXT DEFAULT 'In preparazione'")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE Saggi ADD COLUMN numero_atti INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE Saggi ADD COLUMN durata_totale INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    # Add columns to Coreografie if they don't exist
    try:
        cursor.execute("ALTER TABLE Coreografie ADD COLUMN atto INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE Coreografie ADD COLUMN ordine_uscita INTEGER")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE Coreografie ADD COLUMN musica TEXT")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE Coreografie ADD COLUMN durata INTEGER")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()
    print("Migrazione completata con successo!")

if __name__ == "__main__":
    migrate()
