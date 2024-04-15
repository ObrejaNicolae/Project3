import json
import csv
import spacy

def verifica_tip_db(ultim_cuvant):
    with open('db-tipo.json') as f:
        tipuri_db = json.load(f)
    return ultim_cuvant in tipuri_db

def proceseaza_date(input_file, output_file):
    with open(input_file, 'r') as f:
        date = json.load(f)
        
    descriere = ""
    
    header_fields = set()
    for item in date:
        header_fields.update(item.keys())

    # Sortează antetul pentru a avea aceeași ordine în fișierul CSV
    header_fields = sorted(header_fields)

    # Adaugă un rând suplimentar pentru antetul CSV
    header_row = dict((field, field) for field in header_fields)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header_fields)
        
        # Scrie antetul
        writer.writeheader()
        # Daca expresia este de tip 'campo' atunci se verifica daca ultimul cuvint este un tip database din fisierul db-tipo.json si ultimul cuvant se ignora la verificare
        for row in date:
            if 'tipo'  in row and row['tipo'] == 'campo':
                cuvinte = row['espressione'].split('-')
                ultim_cuvant = cuvinte[-1]
                # Ignorăm ultimul cuvânt la verificare
                cuvinte_de_verificat = cuvinte[:-1]
                cuvant_de_verificat = "-".join(cuvinte_de_verificat)

                if verifica_tip_db(ultim_cuvant):
                    row['stato'] = 'OK'
                else:
                    row['stato'] = 'WARNING', 
                    descriere = "Ca este de tip campo"
            else:
                row['stato'] = 'OK'
            
        # Scrie fiecare rând din date
        for row in date:
            # Completează rândul cu valorile din obiectul JSON
            for field in header_fields:
                header_row[field] = row.get(field, '')
            writer.writerow(header_row)

proceseaza_date('input.json', 'raport.csv')
print('REZULTATELE SUNT IN REZULTAT.CSV')