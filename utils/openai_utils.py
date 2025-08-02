
import pandas as pd

def genereaza_deviz_AI(tip_dulap, dimensiuni, descriere, nume_client, telefon_client):
    df = pd.read_csv("Accesorii.csv")
    materiale = df[df['Producator'].notna()].sample(n=5).to_dict(orient='records')
    lista_finala = []
    total = 0

    for item in materiale:
        cantitate = 2
        pret = item.get('Pret') or item.get('Preț') or item.get('pret') or 0.0
        subtotal = cantitate * float(pret)
        total += subtotal
        lista_finala.append({
            "produs": item.get('Denumire produs') or item.get('Produs') or item.get('Descriere') or "Necunoscut",
            "cod": item.get('Cod produs') or item.get('Cod') or "Fără cod",
            "cantitate": cantitate,
            "pret_unitar": pret,
            "subtotal": subtotal
        })

    return {
        "numar": "",
        "client": nume_client,
        "telefon": telefon_client,
        "tip": tip_dulap,
        "dimensiuni": dimensiuni,
        "prompt": descriere,
        "items": lista_finala,
        "valoare": round(total, 2),
        "valoare_total": round(total, 2)
    }
