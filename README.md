# Progetto Dance Academy
Gestione di una scuola di danza: allieve, maestre, corsi, saggi, pagamenti e certificati.

## Contenuto
- Applicazione Django `academy` con template e static files
- Database SQLite di sviluppo: `Scuola.db` (NON committare in produzione)
- File di dump SQL: `dump.sql` (solo per import/backup)

## Requisiti
- Python 3.10+
- `pip` (gestore pacchetti)
- Windows / macOS / Linux

## Installazione locale (sviluppo)
1. Crea e attiva un ambiente virtuale:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Installa le dipendenze:

```powershell
pip install -r requirements.txt
```

3. Imposta variabili d'ambiente (esempio in PowerShell, temporaneo per la sessione):

```powershell
#$ per sviluppo: sostituisci con valori sicuri in produzione
$env:DJANGO_SECRET_KEY = "replace-with-a-secret"
$env:DJANGO_DEBUG = "True"
```

4. Esegui migrazioni e crea un superuser:

```powershell
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
```

5. Avvia il server di sviluppo:

```powershell
py manage.py runserver
```

Apri `http://127.0.0.1:8000/` nel browser.

## Database e dump
- Il progetto usa SQLite per sviluppo (`Scuola.db`). Non committare file di database nel repository.
- Se hai `dump.sql`, puoi importarne il contenuto in un DB SQLite o usarlo come riferimento. Per SQLite:

```powershell
sqlite3 Scuola.db < dump.sql
```

Nota: ho aggiunto `Scuola.db` e `dump.sql` a `.gitignore` per evitare commit accidentali.

## Sicurezza e produzione
- Non pubblicare `SECRET_KEY` nel repo. Usa variabili d'ambiente (es. `DJANGO_SECRET_KEY`) o un file `.env` escluso da Git.
- Imposta `DJANGO_DEBUG=False` in produzione.
- Rimuovi dati sensibili dalla storia Git se sono già stati committati (vedi prossimo paragrafo).

## Preparare il repository per GitHub
Se hai già committato il DB o il dump, rimuovili dalla storia prima di pubblicare. Comandi consigliati:

```powershell
git rm --cached Scuola.db dump.sql
git commit -m "Remove local DB and dump from repository"
git push
```

Per rimuovere definitivamente dalla storia usa strumenti come `git filter-repo` o `git filter-branch` con attenzione.

## Test
Esegui la suite di test Django:

```powershell
py manage.py test
```

## Contribuire
- Apri una issue per bug o feature
- Fork, branch feature e pull request

## Note finali
- Ho creato/aggiornato alcune buone pratiche nel repo: usare variabili d'ambiente per `SECRET_KEY` e `DEBUG`, e mantenere il DB locale fuori dal controllo versione.
- Se vuoi, posso aggiungere un file `.env.example`, script di setup, o una `LICENSE`.

