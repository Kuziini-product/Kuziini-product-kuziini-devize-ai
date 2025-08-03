import base64
import os
import json
import requests

def incarca_in_github(data):
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or "ghp_xxx..."  # ← înlocuiește cu tokenul tău real
    REPO_OWNER = "Kuziini-product"
    REPO_NAME = "Kuziini-product-kuziini-devize-ai"
    BRANCH = "main"
    FOLDER = "history"

    file_name = f"{data['numar']}_{data['client']}.json"
    file_path = f"{FOLDER}/{file_name}"
    file_content = json.dumps(data, indent=2, ensure_ascii=False)

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    encoded = base64.b64encode(file_content.encode()).decode()

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "message": f"Adaugă deviz {file_name}",
        "content": encoded,
        "branch": BRANCH
    }

    try:
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Devizul a fost încărcat pe GitHub: {file_name}")
        else:
            print(f"❌ Eroare GitHub: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Eroare upload GitHub:", e)
