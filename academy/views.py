from collections import defaultdict
from datetime import date, timedelta

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (
    Allieva,
    AssegnazioneCostume,
    Corso,
    Coreografia,
    Lezione,
    Maestra,
    PagamentoAllieva,
    PagamentoMaestra,
    Saggio,
)


GIORNI_SETTIMANA = {
    0: "Lunedì",
    1: "Martedì",
    2: "Mercoledì",
    3: "Giovedì",
    4: "Venerdì",
    5: "Sabato",
    6: "Domenica",
}
ORDINE_GIORNI = list(GIORNI_SETTIMANA.values())


def _blank_to_none(value):
    return value or None


def _int_or_default(value, default):
    return int(value) if value not in (None, "") else default


def _today():
    return timezone.localdate()


def _stats():
    oggi = _today()
    limite_scadenze = oggi + timedelta(days=7)
    prossimo_saggio = Saggio.objects.order_by("data").first()

    return {
        "allieve": Allieva.objects.count(),
        "maestre": Maestra.objects.count(),
        "corsi": Corso.objects.count(),
        "pagamenti_allieve_scadenza": PagamentoAllieva.objects.filter(
            ~Q(stato="Pagato"), data_scadenza__lte=limite_scadenze
        ).count(),
        "pagamenti_maestre_scadenza": PagamentoMaestra.objects.filter(
            ~Q(stato="Pagato"), data_scadenza__lte=limite_scadenze
        ).count(),
        "lezioni_oggi": Lezione.objects.filter(
            giorno_settimana=GIORNI_SETTIMANA[oggi.weekday()]
        ).count(),
        "costumi_non_consegnati": AssegnazioneCostume.objects.filter(
            consegnato=False
        ).count(),
        "stato_saggio": prossimo_saggio.titolo if prossimo_saggio else "Nessuno",
    }


def _lezioni_oggi():
    return (
        Lezione.objects.select_related("id_corso", "id_maestra")
        .filter(giorno_settimana=GIORNI_SETTIMANA[_today().weekday()])
        .annotate(num_allieve=Count("id_corso__allieve"))
        .order_by("ora_inizio")
    )


def _prossime_scadenze(limit=5):
    pagamenti_allieve = [
        {
            "tipo": "Allieva",
            "nome": pagamento.id_allieva.nome,
            "cognome": pagamento.id_allieva.cognome,
            "importo": pagamento.importo,
            "data_scadenza": pagamento.data_scadenza,
        }
        for pagamento in PagamentoAllieva.objects.select_related("id_allieva").filter(
            ~Q(stato="Pagato")
        )
    ]
    pagamenti_maestre = [
        {
            "tipo": "Maestra",
            "nome": pagamento.id_maestra.nome,
            "cognome": pagamento.id_maestra.cognome,
            "importo": pagamento.importo,
            "data_scadenza": pagamento.data_scadenza,
        }
        for pagamento in PagamentoMaestra.objects.select_related("id_maestra").filter(
            ~Q(stato="Pagato")
        )
    ]
    scadenze = pagamenti_allieve + pagamenti_maestre
    scadenze.sort(key=lambda item: item["data_scadenza"] or date.max)
    return scadenze[:limit]


def _calendario():
    gruppi = defaultdict(list)
    lezioni = Lezione.objects.select_related("id_corso", "id_maestra").order_by(
        "ora_inizio"
    )

    for lezione in lezioni:
        gruppi[lezione.giorno_settimana].append(lezione)

    calendario = {
        giorno: gruppi[giorno] for giorno in ORDINE_GIORNI if giorno in gruppi
    }
    for giorno, lezioni_giorno in gruppi.items():
        if giorno not in calendario:
            calendario[giorno] = lezioni_giorno
    return calendario


def _saggi_completi():
    saggi = list(Saggio.objects.all())
    for saggio in saggi:
        coreografie = (
            saggio.coreografie.select_related("id_corso", "id_maestra")
            .annotate(num_allieve=Count("id_corso__allieve"))
            .order_by("atto", "ordine_uscita")
        )
        atti = defaultdict(list)
        for coreografia in coreografie:
            atti[coreografia.atto].append(coreografia)
        saggio.atti = dict(sorted(atti.items()))
    return saggi


def index(request):
    return render(
        request,
        "index.html",
        {
            "stats": _stats(),
            "lezioni_oggi": _lezioni_oggi(),
            "scadenze": _prossime_scadenze(5),
        },
    )


def calendario(request):
    return render(request, "calendario.html", {"calendario": _calendario()})


def allieve(request):
    return render(
        request,
        "allieve.html",
        {"allieve": Allieva.objects.select_related("id_corso").all()},
    )


def maestre(request):
    return render(request, "maestre.html", {"maestre": Maestra.objects.all()})


def corsi(request):
    return render(
        request,
        "corsi.html",
        {"corsi": Corso.objects.select_related("id_maestra").all()},
    )


def pagamenti_allieve(request):
    return render(
        request,
        "pagamenti_allieve.html",
        {
            "pagamenti": PagamentoAllieva.objects.select_related(
                "id_allieva"
            ).all()
        },
    )


def pagamenti_maestre(request):
    return render(
        request,
        "pagamenti_maestre.html",
        {
            "pagamenti": PagamentoMaestra.objects.select_related(
                "id_maestra"
            ).all()
        },
    )


def saggio(request):
    return render(request, "saggio.html", {"saggi": _saggi_completi()})


def costumi(request):
    return render(
        request,
        "costumi.html",
        {
            "costumi": AssegnazioneCostume.objects.select_related(
                "id_allieva", "id_costume", "id_coreografia"
            ).all()
        },
    )


def certificati(request):
    oggi = _today()
    allieve_critiche = Allieva.objects.filter(
        Q(certificato_medico__isnull=True) | Q(certificato_medico__lt=oggi)
    ).order_by("certificato_medico", "cognome")
    return render(request, "certificati.html", {"allieve": allieve_critiche})


def allieva_dettaglio(request, id_allieva):
    allieva = get_object_or_404(
        Allieva.objects.select_related("id_corso"), pk=id_allieva
    )
    dati = {
        "info": allieva,
        "pagamenti": allieva.pagamenti.all(),
        "costumi": AssegnazioneCostume.objects.select_related(
            "id_costume", "id_coreografia"
        ).filter(id_allieva=allieva),
    }
    return render(request, "allieva_dettaglio.html", {"dati": dati})


@require_POST
def aggiorna_certificato(request, id_allieva):
    data = request.POST.get("data_scadenza")
    if data:
        Allieva.objects.filter(pk=id_allieva).update(certificato_medico=data)
    return redirect("allieva_dettaglio", id_allieva=id_allieva)


def paga_allieva(request, id_pagamento):
    pagamento = get_object_or_404(PagamentoAllieva, pk=id_pagamento)
    pagamento.stato = "Pagato"
    pagamento.data_pagamento = _today()
    pagamento.save(update_fields=["stato", "data_pagamento"])
    return redirect("pagamenti_allieve")


def paga_maestra(request, id_pagamento):
    pagamento = get_object_or_404(PagamentoMaestra, pk=id_pagamento)
    pagamento.stato = "Pagato"
    pagamento.data_pagamento = _today()
    pagamento.save(update_fields=["stato", "data_pagamento"])
    return redirect("pagamenti_maestre")


def nuova_allieva(request):
    if request.method == "POST":
        Allieva.objects.create(
            nome=request.POST.get("nome"),
            cognome=request.POST.get("cognome"),
            data_nascita=_blank_to_none(request.POST.get("data_nascita")),
            telefono=_blank_to_none(request.POST.get("telefono")),
            email=_blank_to_none(request.POST.get("email")),
            data_iscrizione=_blank_to_none(request.POST.get("data_iscrizione")),
            id_corso_id=request.POST.get("id_corso"),
            certificato_medico=_blank_to_none(
                request.POST.get("certificato_medico")
            ),
        )
        return redirect("allieve")

    return render(
        request,
        "nuova_allieva.html",
        {"corsi": Corso.objects.select_related("id_maestra").all()},
    )


def nuova_maestra(request):
    if request.method == "POST":
        Maestra.objects.create(
            nome=request.POST.get("nome"),
            cognome=request.POST.get("cognome"),
            telefono=_blank_to_none(request.POST.get("telefono")),
            email=_blank_to_none(request.POST.get("email")),
            specializzazione=_blank_to_none(request.POST.get("specializzazione")),
            compenso_mensile=_blank_to_none(request.POST.get("compenso_mensile")),
        )
        return redirect("maestre")

    return render(request, "nuova_maestra.html")


def nuovo_corso(request):
    if request.method == "POST":
        Corso.objects.create(
            nome=request.POST.get("nome"),
            livello=_blank_to_none(request.POST.get("livello")),
            fascia_eta=_blank_to_none(request.POST.get("fascia_eta")),
            id_maestra_id=request.POST.get("id_maestra"),
        )
        return redirect("corsi")

    return render(request, "nuovo_corso.html", {"maestre": Maestra.objects.all()})


def nuovo_saggio(request):
    if request.method == "POST":
        Saggio.objects.create(
            titolo=request.POST.get("titolo"),
            data=_blank_to_none(request.POST.get("data")),
            luogo=_blank_to_none(request.POST.get("luogo")),
            ora_inizio=_blank_to_none(request.POST.get("ora_inizio")),
            stato=_blank_to_none(request.POST.get("stato")) or "In preparazione",
            numero_atti=_int_or_default(request.POST.get("numero_atti"), 1),
            durata_totale=_int_or_default(request.POST.get("durata_totale"), 0),
        )
        return redirect("saggio")

    return render(request, "nuovo_saggio.html")


def nuova_coreografia(request):
    if request.method == "POST":
        Coreografia.objects.create(
            nome=request.POST.get("nome"),
            id_saggio_id=request.POST.get("id_saggio"),
            id_corso_id=request.POST.get("id_corso"),
            id_maestra_id=request.POST.get("id_maestra"),
            atto=_int_or_default(request.POST.get("atto"), 1),
            ordine_uscita=_blank_to_none(request.POST.get("ordine_uscita")),
            musica=_blank_to_none(request.POST.get("musica")),
            durata=_blank_to_none(request.POST.get("durata")),
        )
        return redirect("saggio")

    return render(
        request,
        "nuova_coreografia.html",
        {
            "saggi": Saggio.objects.all(),
            "corsi": Corso.objects.all(),
            "maestre": Maestra.objects.all(),
        },
    )


def modifica_coreografia(request, id_coreografia):
    coreo = get_object_or_404(Coreografia, pk=id_coreografia)

    if request.method == "POST":
        coreo.nome = request.POST.get("nome")
        coreo.id_corso_id = request.POST.get("id_corso")
        coreo.id_maestra_id = request.POST.get("id_maestra")
        coreo.atto = _int_or_default(request.POST.get("atto"), 1)
        coreo.ordine_uscita = _blank_to_none(request.POST.get("ordine_uscita"))
        coreo.musica = _blank_to_none(request.POST.get("musica"))
        coreo.durata = _blank_to_none(request.POST.get("durata"))
        coreo.save(
            update_fields=[
                "nome",
                "id_corso",
                "id_maestra",
                "atto",
                "ordine_uscita",
                "musica",
                "durata",
            ]
        )
        return redirect("saggio")

    return render(
        request,
        "modifica_coreografia.html",
        {
            "coreo": coreo,
            "corsi": Corso.objects.all(),
            "maestre": Maestra.objects.all(),
        },
    )
