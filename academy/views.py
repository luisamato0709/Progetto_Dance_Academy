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
