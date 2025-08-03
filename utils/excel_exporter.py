import pandas as pd

def export_excel(data):
    rows = []
    total = 0.0

    for item in data.get("items", []):
        produs = item.get("produs", "—")
        cant = item.get("cantitate", 1)
        pret = item.get("preț") or item.get("pret") or 0
        total_individual = float(cant) * float(pret)
        total += total_individual

        rows.append({
            "Produs": produs,
            "Cantitate": cant,
            "Preț unitar": pret,
            "Total": total_individual
        })

    df = pd.DataFrame(rows)

    # Adăugăm rândul total general
    total_df = pd.DataFrame([{
        "Produs": "TOTAL GENERAL",
        "Cantitate": "",
        "Preț unitar": "",
        "Total": round(total, 2)
    }])

    df = pd.concat([df, total_df], ignore_index=True)

    file_path = f"exports/{data['numar']}_{data['client']}.xlsx"
    df.to_excel(file_path, index=False)
