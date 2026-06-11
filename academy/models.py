from django.db import models
from django.utils import timezone


class Maestra(models.Model):
    """Modello per le insegnanti della scuola di danza"""
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    specializzazione = models.CharField(max_length=100, blank=True, null=True)
    compenso_mensile = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name_plural = "Maestre"
    
    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Corso(models.Model):
    """Modello per i corsi di danza"""
    LIVELLI = [
        ('Base', 'Base'),
        ('Intermedio', 'Intermedio'),
        ('Avanzato', 'Avanzato'),
        ('Tutti', 'Tutti'),
    ]
    
    nome = models.CharField(max_length=150)
    livello = models.CharField(max_length=50, choices=LIVELLI, blank=True, null=True)
    fascia_eta = models.CharField(max_length=100, blank=True, null=True)
    id_maestra = models.ForeignKey(Maestra, on_delete=models.SET_NULL, null=True, related_name='corsi')
    
    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Allieva(models.Model):
    """Modello per le allieve della scuola di danza"""
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    data_nascita = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data_iscrizione = models.DateField(blank=True, null=True)
    id_corso = models.ForeignKey(Corso, on_delete=models.SET_NULL, null=True, related_name='allieve')
    certificato_medico = models.DateField(blank=True, null=True, help_text="Data di scadenza del certificato medico")
    
    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name_plural = "Allieve"
    
    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Lezione(models.Model):
    """Modello per le lezioni"""
    GIORNI_SETTIMANA = [
        ('Lunedì', 'Lunedì'),
        ('Martedì', 'Martedì'),
        ('Mercoledì', 'Mercoledì'),
        ('Giovedì', 'Giovedì'),
        ('Venerdì', 'Venerdì'),
        ('Sabato', 'Sabato'),
        ('Domenica', 'Domenica'),
    ]
    
    giorno_settimana = models.CharField(max_length=20, choices=GIORNI_SETTIMANA)
    ora_inizio = models.TimeField()
    ora_fine = models.TimeField()
    sala = models.CharField(max_length=50, blank=True, null=True)
    id_corso = models.ForeignKey(Corso, on_delete=models.CASCADE, related_name='lezioni')
    id_maestra = models.ForeignKey(Maestra, on_delete=models.SET_NULL, null=True, related_name='lezioni')
    
    class Meta:
        ordering = ['giorno_settimana', 'ora_inizio']
    
    def __str__(self):
        return f"{self.id_corso.nome} - {self.giorno_settimana} {self.ora_inizio}"


class PagamentoAllieva(models.Model):
    """Modello per i pagamenti delle allieve"""
    STATI = [
        ('Da pagare', 'Da pagare'),
        ('Pagato', 'Pagato'),
        ('In ritardo', 'In ritardo'),
    ]
    
    id_allieva = models.ForeignKey(Allieva, on_delete=models.CASCADE, related_name='pagamenti')
    importo = models.DecimalField(max_digits=8, decimal_places=2)
    data_scadenza = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    stato = models.CharField(max_length=50, choices=STATI, default='Da pagare')
    descrizione = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ['-data_scadenza']
    
    def __str__(self):
        return f"Pagamento {self.id_allieva.cognome} - {self.descrizione}"


class PagamentoMaestra(models.Model):
    """Modello per i pagamenti delle maestre"""
    STATI = [
        ('Da pagare', 'Da pagare'),
        ('Pagato', 'Pagato'),
        ('In ritardo', 'In ritardo'),
    ]
    
    id_maestra = models.ForeignKey(Maestra, on_delete=models.CASCADE, related_name='pagamenti')
    importo = models.DecimalField(max_digits=8, decimal_places=2)
    data_scadenza = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    stato = models.CharField(max_length=50, choices=STATI, default='Da pagare')
    descrizione = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ['-data_scadenza']
    
    def __str__(self):
        return f"Pagamento {self.id_maestra.cognome} - {self.descrizione}"


class Saggio(models.Model):
    """Modello per i saggi (spettacoli)"""
    STATI = [
        ('In preparazione', 'In preparazione'),
        ('Programmato', 'Programmato'),
        ('Completato', 'Completato'),
        ('Rinviato', 'Rinviato'),
    ]
    
    titolo = models.CharField(max_length=200)
    data = models.DateField(blank=True, null=True)
    luogo = models.CharField(max_length=200, blank=True, null=True)
    ora_inizio = models.TimeField(blank=True, null=True)
    stato = models.CharField(max_length=50, choices=STATI, default='In preparazione')
    numero_atti = models.IntegerField(default=1)
    durata_totale = models.IntegerField(default=0, help_text="Durata in minuti")
    
    class Meta:
        ordering = ['data']
    
    def __str__(self):
        return self.titolo


class Coreografia(models.Model):
    """Modello per le coreografie"""
    nome = models.CharField(max_length=200)
    id_saggio = models.ForeignKey(Saggio, on_delete=models.CASCADE, related_name='coreografie')
    id_corso = models.ForeignKey(Corso, on_delete=models.SET_NULL, null=True, related_name='coreografie')
    id_maestra = models.ForeignKey(Maestra, on_delete=models.SET_NULL, null=True, related_name='coreografie')
    atto = models.IntegerField(default=1)
    ordine_uscita = models.IntegerField(blank=True, null=True)
    musica = models.CharField(max_length=200, blank=True, null=True)
    durata = models.IntegerField(blank=True, null=True, help_text="Durata in secondi")
    
    class Meta:
        ordering = ['id_saggio', 'atto', 'ordine_uscita']
        verbose_name_plural = "Coreografie"
    
    def __str__(self):
        return f"{self.nome} - {self.id_saggio.titolo}"


class Costume(models.Model):
    """Modello per i costumi"""
    STATI_ORDINE = [
        ('In magazzino', 'In magazzino'),
        ('Ordinato', 'Ordinato'),
        ('Consegnato', 'Consegnato'),
        ('In uso', 'In uso'),
    ]
    
    nome = models.CharField(max_length=200)
    descrizione = models.TextField(blank=True, null=True)
    taglia = models.CharField(max_length=10, blank=True, null=True)
    prezzo = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fornitore = models.CharField(max_length=150, blank=True, null=True)
    stato_ordine = models.CharField(max_length=50, choices=STATI_ORDINE, default='In magazzino')
    
    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class AssegnazioneCostume(models.Model):
    """Modello per l'assegnazione dei costumi alle allieve"""
    id_allieva = models.ForeignKey(Allieva, on_delete=models.CASCADE, related_name='costumi_assegnati')
    id_costume = models.ForeignKey(Costume, on_delete=models.CASCADE, related_name='assegnazioni')
    id_coreografia = models.ForeignKey(Coreografia, on_delete=models.CASCADE, related_name='assegnazioni_costumi')
    pagato = models.BooleanField(default=False)
    consegnato = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Assegnazioni Costumi"
    
    def __str__(self):
        return f"{self.id_allieva.cognome} - {self.id_costume.nome}"