import db_manager
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


def index(request):
    return render(
        request,
        "index.html",
        {
            "stats": db_manager.get_stats(),
            "lezioni_oggi": db_manager.get_lezioni_oggi_completo(),
            "scadenze": db_manager.get_prossime_scadenze(5),
        },
    )


def calendario(request):
    return render(request, "calendario.html", {"calendario": db_manager.get_calendario()})


def allieve(request):
    return render(request, "allieve.html", {"allieve": db_manager.get_allieve()})


def maestre(request):
    return render(request, "maestre.html", {"maestre": db_manager.get_maestre()})


def corsi(request):
    return render(request, "corsi.html", {"corsi": db_manager.get_corsi()})


def pagamenti_allieve(request):
    return render(
        request,
        "pagamenti_allieve.html",
        {"pagamenti": db_manager.get_pagamenti_allieve()},
    )


def pagamenti_maestre(request):
    return render(
        request,
        "pagamenti_maestre.html",
        {"pagamenti": db_manager.get_pagamenti_maestre()},
    )


def saggio(request):
    return render(request, "saggio.html", {"saggi": db_manager.get_saggi_completo()})


def costumi(request):
    return render(request, "costumi.html", {"costumi": db_manager.get_costumi_completo()})


def certificati(request):
    return render(
        request,
        "certificati.html",
        {"allieve": db_manager.get_allieve_certificati_critici()},
    )


def allieva_dettaglio(request, id_allieva):
    dati = db_manager.get_allieva_details(id_allieva)
    if not dati:
        raise Http404("Allieva non trovata")
    return render(request, "allieva_dettaglio.html", {"dati": dati})


@require_POST
def aggiorna_certificato(request, id_allieva):
    data = request.POST.get("data_scadenza")
    if data:
        db_manager.update_certificato(id_allieva, data)
    return redirect("allieva_dettaglio", id_allieva=id_allieva)


def paga_allieva(request, id_pagamento):
    db_manager.set_pagamento_allieva(id_pagamento)
    return redirect("pagamenti_allieve")


def paga_maestra(request, id_pagamento):
    db_manager.set_pagamento_maestra(id_pagamento)
    return redirect("pagamenti_maestre")
def nuova_allieva(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cognome = request.POST.get("cognome")
        data_nascita = request.POST.get("data_nascita")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        data_iscrizione = request.POST.get("data_iscrizione")
        id_corso = request.POST.get("id_corso")
        certificato_medico = request.POST.get("certificato_medico")
        
        db_manager.add_allieva(nome, cognome, data_nascita, telefono, email, data_iscrizione, id_corso, certificato_medico)
        return redirect("allieve")
        
    return render(request, "nuova_allieva.html", {"corsi": db_manager.get_corsi()})
def nuova_maestra(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cognome = request.POST.get("cognome")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        specializzazione = request.POST.get("specializzazione")
        compenso_mensile = request.POST.get("compenso_mensile")
        
        db_manager.add_maestra(nome, cognome, telefono, email, specializzazione, compenso_mensile)
        return redirect("maestre")
        
    return render(request, "nuova_maestra.html")


def nuovo_corso(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        livello = request.POST.get("livello")
        fascia_eta = request.POST.get("fascia_eta")
        id_maestra = request.POST.get("id_maestra")
        
        db_manager.add_corso(nome, livello, fascia_eta, id_maestra)
        return redirect("corsi")
        
    return render(request, "nuovo_corso.html", {"maestre": db_manager.get_maestre()})
def nuovo_saggio(request):
    if request.method == "POST":
        titolo = request.POST.get("titolo")
        data = request.POST.get("data")
        luogo = request.POST.get("luogo")
        ora_inizio = request.POST.get("ora_inizio")
        stato = request.POST.get("stato")
        numero_atti = request.POST.get("numero_atti")
        durata_totale = request.POST.get("durata_totale")
        
        db_manager.add_saggio(titolo, data, luogo, ora_inizio, stato, numero_atti, durata_totale)
        return redirect("saggio")
        
    return render(request, "nuovo_saggio.html")


def nuova_coreografia(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        id_saggio = request.POST.get("id_saggio")
        id_corso = request.POST.get("id_corso")
        id_maestra = request.POST.get("id_maestra")
        atto = request.POST.get("atto")
        ordine_uscita = request.POST.get("ordine_uscita")
        musica = request.POST.get("musica")
        durata = request.POST.get("durata")
        
        db_manager.add_coreografia(nome, id_saggio, id_corso, id_maestra, atto, ordine_uscita, musica, durata)
        return redirect("saggio")
        
    return render(request, "nuova_coreografia.html", {
        "saggi": db_manager.get_saggi_completo(),
        "corsi": db_manager.get_corsi(),
        "maestre": db_manager.get_maestre()
    })


def modifica_coreografia(request, id_coreografia):
    coreo = db_manager.get_coreografia(id_coreografia)
    if not coreo:
        raise Http404("Coreografia non trovata")
        
    if request.method == "POST":
        nome = request.POST.get("nome")
        id_corso = request.POST.get("id_corso")
        id_maestra = request.POST.get("id_maestra")
        atto = request.POST.get("atto")
        ordine_uscita = request.POST.get("ordine_uscita")
        musica = request.POST.get("musica")
        durata = request.POST.get("durata")
        
        db_manager.update_coreografia(id_coreografia, nome, id_corso, id_maestra, atto, ordine_uscita, musica, durata)
        return redirect("saggio")
        
    return render(request, "modifica_coreografia.html", {
        "coreo": coreo,
        "corsi": db_manager.get_corsi(),
        "maestre": db_manager.get_maestre()
    })
