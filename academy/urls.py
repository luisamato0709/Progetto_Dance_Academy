from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("calendario/", views.calendario, name="calendario"),
    path("allieve/", views.allieve, name="allieve"),
    path("maestre/", views.maestre, name="maestre"),
    path("corsi/", views.corsi, name="corsi"),
    path("pagamenti-allieve/", views.pagamenti_allieve, name="pagamenti_allieve"),
    path("pagamenti-maestre/", views.pagamenti_maestre, name="pagamenti_maestre"),
    path("saggio/", views.saggio, name="saggio"),
    path("costumi/", views.costumi, name="costumi"),
    path("certificati/", views.certificati, name="certificati"),
    path("allieva/<int:id_allieva>/", views.allieva_dettaglio, name="allieva_dettaglio"),
    path(
        "allieva/<int:id_allieva>/aggiorna-certificato/",
        views.aggiorna_certificato,
        name="aggiorna_certificato",
    ),
    path("paga-allieva/<int:id_pagamento>/", views.paga_allieva, name="paga_allieva"),
    path("paga-maestra/<int:id_pagamento>/", views.paga_maestra, name="paga_maestra"),
    path("nuova-allieva/", views.nuova_allieva, name="nuova_allieva"),
    path("nuova-maestra/", views.nuova_maestra, name="nuova_maestra"),
    path("nuovo-corso/", views.nuovo_corso, name="nuovo_corso"),
    path("nuovo-saggio/", views.nuovo_saggio, name="nuovo_saggio"),
    path("nuova-coreografia/", views.nuova_coreografia, name="nuova_coreografia"),
    path("modifica-coreografia/<int:id_coreografia>/", views.modifica_coreografia, name="modifica_coreografia"),
]
