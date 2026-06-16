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
        db_table = 'Maestre'
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
    id_maestra = models.ForeignKey(Maestra, on_delete=models.SET_NULL, null=True, related_name='corsi', db_column='id_maestra')
    
    class Meta:
        db_table = 'Corsi'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

    @property
    def nome_maestra(self):
        return self.id_maestra.nome if self.id_maestra else ""

    @property
    def cognome_maestra(self):
        return self.id_maestra.cognome if self.id_maestra else ""


class Allieva(models.Model):
    """Modello per le allieve della scuola di danza"""
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    data_nascita = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data_iscrizione = models.DateField(blank=True, null=True)
    id_corso = models.ForeignKey(Corso, on_delete=models.SET_NULL, null=True, related_name='allieve', db_column='id_corso')
    certificato_medico = models.DateField(blank=True, null=True, help_text="Data di scadenza del certificato medico")
    
    class Meta:
        db_table = 'Allieve'
        ordering = ['cognome', 'nome']
        verbose_name_plural = "Allieve"
    
    def __str__(self):
        return f"{self.nome} {self.cognome}"

    @property
    def nome_corso(self):
        return self.id_corso.nome if self.id_corso else ""


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
    id_corso = models.ForeignKey(Corso, on_delete=models.CASCADE, related_name='lezioni', db_column='id_corso')
    id_maestra = models.ForeignKey(Maestra, on_delete=models.SET_NULL, null=True, related_name='lezioni', db_column='id_maestra')
    
    class Meta:
        db_table = 'Lezioni'
        ordering = ['giorno_settimana', 'ora_inizio']
    
    def __str__(self):
        return f"{self.id_corso.nome} - {self.giorno_settimana} {self.ora_inizio}"

    @property
    def nome_corso(self):
        return self.id_corso.nome if self.id_corso else ""

    @property
    def nome_maestra(self):
        return self.id_maestra.nome if self.id_maestra else ""

    @property
    def cognome_maestra(self):
        return self.id_maestra.cognome if self.id_maestra else ""


class PagamentoAllieva(models.Model):
    """Modello per i pagamenti delle allieve"""
    STATI = [
        ('Da pagare', 'Da pagare'),
        ('Pagato', 'Pagato'),
        ('In ritardo', 'In ritardo'),
    ]
    
    id_allieva = models.ForeignKey(Allieva, on_delete=models.CASCADE, related_name='pagamenti', db_column='id_allieva')
    importo = models.DecimalField(max_digits=8, decimal_places=2)
    data_scadenza = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    stato = models.CharField(max_length=50, choices=STATI, default='Da pagare')
    descrizione = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        db_table = 'Pagamenti_Allieve'
        ordering = ['-data_scadenza']
    
    def __str__(self):
        return f"Pagamento {self.id_allieva.cognome} - {self.descrizione}"

    @property
    def nome_allieva(self):
        return self.id_allieva.nome if self.id_allieva else ""

    @property
    def cognome_allieva(self):
        return self.id_allieva.cognome if self.id_allieva else ""


class PagamentoMaestra(models.Model):
    """Modello per i pagamenti delle maestre"""
    STATI = [
        ('Da pagare', 'Da pagare'),
        ('Pagato', 'Pagato'),
        ('In ritardo', 'In ritardo'),
    ]
    
    id_maestra = models.ForeignKey(Maestra, on_delete=models.CASCADE, related_name='pagamenti', db_column='id_maestra')
    importo = models.DecimalField(max_digits=8, decimal_places=2)
    data_scadenza = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    stato = models.CharField(max_length=50, choices=STATI, default='Da pagare')
    descrizione = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        db_table = 'Pagamenti_Maestre'
        ordering = ['-data_scadenza']
    
    def __str__(self):
        return f"Pagamento {self.id_maestra.cognome} - {self.descrizione}"

    @property
    def nome_maestra(self):
        return self.id_maestra.nome if self.id_maestra else ""

    @property
    def cognome_maestra(self):
        return self.id_maestra.cognome if self.id_maestra else ""


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
        db_table = 'Saggi'
        ordering = ['data']
    
    def __str__(self):
        return self.titolo


class Coreografia(models.Model):
    """Modello per le coreografie"""
    nome = models.CharField(max_length=200)
    id_saggio = models.ForeignKey(Saggio, on_delete=models.CASCADE, related_name='coreografie', db_column='id_saggio')
    id_corso = models.ForeignKey(Corso, on_delete=models.SET_NULL, null=True, related_name='coreografie', db_column='id_corso')
    id_maestra = models.ForeignKey(Maestra, on_delete=models.SET_NULL, null=True, related_name='coreografie', db_column='id_maestra')
    atto = models.IntegerField(default=1)
    ordine_uscita = models.IntegerField(blank=True, null=True)
    musica = models.CharField(max_length=200, blank=True, null=True)
    durata = models.IntegerField(blank=True, null=True, help_text="Durata in secondi")
    
    class Meta:
        db_table = 'Coreografie'
        ordering = ['id_saggio', 'atto', 'ordine_uscita']
        verbose_name_plural = "Coreografie"
    
    def __str__(self):
        return f"{self.nome} - {self.id_saggio.titolo}"

    @property
    def nome_corso(self):
        return self.id_corso.nome if self.id_corso else ""

    @property
    def nome_maestra(self):
        return self.id_maestra.nome if self.id_maestra else ""

    @property
    def cognome_maestra(self):
        return self.id_maestra.cognome if self.id_maestra else ""


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
        db_table = 'Costumi'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class AssegnazioneCostume(models.Model):
    """Modello per l'assegnazione dei costumi alle allieve"""
    id_allieva = models.ForeignKey(Allieva, on_delete=models.CASCADE, related_name='costumi_assegnati', db_column='id_allieva')
    id_costume = models.ForeignKey(Costume, on_delete=models.CASCADE, related_name='assegnazioni', db_column='id_costume')
    id_coreografia = models.ForeignKey(Coreografia, on_delete=models.CASCADE, related_name='assegnazioni_costumi', db_column='id_coreografia')
    pagato = models.BooleanField(default=False)
    consegnato = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Assegnazione_Costumi'
        verbose_name_plural = "Assegnazioni Costumi"
    
    def __str__(self):
        return f"{self.id_allieva.cognome} - {self.id_costume.nome}"

    @property
    def nome_allieva(self):
        return self.id_allieva.nome if self.id_allieva else ""

    @property
    def cognome_allieva(self):
        return self.id_allieva.cognome if self.id_allieva else ""

    @property
    def nome_costume(self):
        return self.id_costume.nome if self.id_costume else ""

    @property
    def taglia(self):
        return self.id_costume.taglia if self.id_costume else ""

    @property
    def prezzo(self):
        return self.id_costume.prezzo if self.id_costume else None

    @property
    def nome_coreografia(self):
        return self.id_coreografia.nome if self.id_coreografia else ""


class Competizione(models.Model):
    """Modello per le competizioni"""
    id_concorso = models.AutoField(primary_key=True)
    classifica = models.IntegerField(blank=True, null=True)
    numero_giudici = models.IntegerField()

    class Meta:
        db_table = 'Competizione'

    def __str__(self):
        return f"Competizione {self.id_concorso}"


class IscrizioneCompetizione(models.Model):
    """Modello per le iscrizioni alle competizioni"""
    id_allieva = models.ForeignKey(Allieva, on_delete=models.CASCADE, related_name='iscrizioni_competizioni', db_column='id_allieva')
    id_concorso = models.ForeignKey(Competizione, on_delete=models.CASCADE, related_name='iscrizioni', db_column='id_concorso')

    class Meta:
        db_table = 'Iscrizione_Competizione'
        unique_together = (('id_allieva', 'id_concorso'),)

    def __str__(self):
        return f"{self.id_allieva} -> {self.id_concorso}"
