# -*- coding: utf-8 -*-
"""PROGETTO3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OOND0Btil9z_3ni3x37AQX-ZnMgGSHIh
"""

from google.colab import files
uploaded = files.upload()
import os
print(os.listdir('/content'))

import csv

def leggi_csv(file_path):
    dati = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Salta l'intestazione se presente
        for riga in reader:
            dati.append(riga)
    return dati

file_path = '/content/telefonate.csv'  # Usa il percorso corretto
dati_telefonate = leggi_csv(file_path)
print(dati_telefonate[:5])  # Stampa le prime 5 righe per controllo

def minuti_da_inizio_mese(g, h, m):
    """Calcola i minuti dall'inizio del mese."""
    return g * 24 * 60 + h * 60 + m

def ottieniDatiTelefonate(nomeFile):
    """Legge il file CSV e restituisce una lista di tuple con le informazioni valide sulle telefonate."""
    dati = []
    with open(nomeFile, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Salta l'intestazione
        for row in reader:
            if row[0].startswith('#'):
                continue  # Ignora righe di errore
            try:
                cod_chiamante, cod_destinatario = int(row[0]), int(row[1])
                cod_cella_chiamante, cod_cella_destinatario = int(row[2]), int(row[3])
                ggi, hhi, mmi = int(row[4]), int(row[5]), int(row[6])
                ggf, hhf, mmf = int(row[7]), int(row[8]), int(row[9])

                if cod_chiamante == cod_destinatario:
                    continue  # Esclude chiamate a se stessi
                if not (1 <= ggi <= 31 and 1 <= ggf <= 31 and 0 <= hhi < 24 and 0 <= hhf < 24 and 0 <= mmi < 60 and 0 <= mmf < 60):
                    continue  # Esclude dati errati

                minuti_inizio = minuti_da_inizio_mese(ggi, hhi, mmi)
                minuti_fine = minuti_da_inizio_mese(ggf, hhf, mmf)
                if minuti_fine < minuti_inizio or minuti_fine - minuti_inizio > 600:
                    continue  # Esclude chiamate troppo lunghe o troppo corte

                durata = 0
                durata = minuti_fine - minuti_inizio + 1
                dati.append((cod_chiamante, cod_destinatario, cod_cella_chiamante, cod_cella_destinatario, durata))
            except ValueError:
                continue
    return dati

def calcolaBollette(datiChiamate):
    """Calcola la bolletta dei clienti in base ai minuti di chiamata."""
    bollette = {}
    for chiamante, _, _, _, durata in datiChiamate:
        if chiamante not in bollette:
            bollette[chiamante] = 0
        minuti_tariffati = max(durata - 20, 0)
        bollette[chiamante] += minuti_tariffati * 0.10
    return bollette

def calcolaCelleCongestionate(datiChiamate):
    for _, _, cella, _, _ in datiChiamate:
        {}[cella] = {}.get(cella, 0) + 1
    if not {}:
        return []
    media_chiamate = sum({}.values()) / len({})
    return [cella for cella, conteggio in {}.items() if conteggio > media_chiamate]


# Esempio di utilizzo:
nome_file = "telefonate.csv"
dati = ottieniDatiTelefonate(nome_file)
stampa_bollette = calcolaBollette(dati)
stampa_celle_congestionate = calcolaCelleCongestionate(dati)

print("Bollette:", stampa_bollette)
print("Celle Congestionate:", stampa_celle_congestionate)