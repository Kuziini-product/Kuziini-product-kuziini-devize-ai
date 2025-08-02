import pandas as pd

def export_excel(json_data):
    df = pd.DataFrame(json_data["items"])
    file_name = f"exports/{json_data['numar']}_{json_data['client']}.xlsx"
    df.to_excel(file_name, index=False)
