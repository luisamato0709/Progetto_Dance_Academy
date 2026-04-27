from flask import Flask, render_template, request, redirect, url_for
import db_manager
import webbrowser
import threading
from datetime import date
import sqlite3 

app = Flask(__name__)

@app.context_processor
def inject_today():
    return {'date_today': date.today().isoformat()}

@app.route('/')
def index():
    stats = db_manager.get_stats()
    lezioni_oggi = db_manager.get_lezioni_oggi_completo()
    scadenze = db_manager.get_prossime_scadenze(5)
    return render_template('index.html', stats=stats, lezioni_oggi=lezioni_oggi, scadenze=scadenze)

@app.route('/calendario')
def calendario():
    programma = db_manager.get_calendario()
    return render_template('calendario.html', calendario=programma)

@app.route('/allieve')
def allieve():
    lista_allieve = db_manager.get_allieve()
    return render_template('allieve.html', allieve=lista_allieve)

@app.route('/maestre')
def maestre():
    lista_maestre = db_manager.get_maestre()
    return render_template('maestre.html', maestre=lista_maestre)

@app.route('/corsi')
def corsi():
    lista_corsi = db_manager.get_corsi()
    return render_template('corsi.html', corsi=lista_corsi)

@app.route('/pagamenti-allieve')
def pagamenti_allieve():
    pagamenti = db_manager.get_pagamenti_allieve()
    return render_template('pagamenti_allieve.html', pagamenti=pagamenti)

@app.route('/pagamenti-maestre')
def pagamenti_maestre():
    pagamenti = db_manager.get_pagamenti_maestre()
    return render_template('pagamenti_maestre.html', pagamenti=pagamenti)

@app.route('/saggio')
def saggio():
    saggi = db_manager.get_saggi_completo()
    return render_template('saggio.html', saggi=saggi)

@app.route('/costumi')
def costumi():
    costumi = db_manager.get_costumi_completo()
    return render_template('costumi.html', costumi=costumi)

@app.route('/certificati')
def certificati():
    allieve_critiche = db_manager.get_allieve_certificati_critici()
    return render_template('certificati.html', allieve=allieve_critiche)

@app.route('/allieva/<int:id_allieva>')
def allieva_dettaglio(id_allieva):
    dati = db_manager.get_allieva_details(id_allieva)
    if not dati:
        return "Allieva non trovata", 404
    return render_template('allieva_dettaglio.html', dati=dati)

@app.route('/allieva/<int:id_allieva>/aggiorna_certificato', methods=['POST'])
def aggiorna_certificato(id_allieva):
    data = request.form.get('data_scadenza')
    if data:
        db_manager.update_certificato(id_allieva, data)
    return redirect(url_for('allieva_dettaglio', id_allieva=id_allieva))

@app.route('/paga_allieva/<int:id_pagamento>')
def paga_allieva(id_pagamento):
    db_manager.set_pagamento_allieva(id_pagamento)
    return redirect(url_for('pagamenti_allieve'))

@app.route('/paga_maestra/<int:id_pagamento>')
def paga_maestra(id_pagamento):
    db_manager.set_pagamento_maestra(id_pagamento)
    return redirect(url_for('pagamenti_maestre'))

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # threading.Timer(1.25, open_browser).start()
    app.run(debug=True, port=5000, use_reloader=False)
