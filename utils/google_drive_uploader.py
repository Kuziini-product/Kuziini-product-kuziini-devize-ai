# uploader with my@kuziini.ro integrationimport os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Setările folderului rădăcină (partajat de my@kuziini.ro)
FOLDER_ROOT = "Kuziini_Devize"

def incarca_in_google_drive(json_data):
    creds = service_account.Credentials.from_service_account_file(
        "client_secrets.json",
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=creds)

    year = "2025"
    client = json_data["client"]
    folder_structure = [FOLDER_ROOT, year, client]
    parent_id = None

    for folder in folder_structure:
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder}'"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        results = service.files().list(q=query, fields="files(id)").execute()
        items = results.get("files", [])

        if items:
            parent_id = items[0]["id"]
        else:
            file_metadata = {
                "name": folder,
                "mimeType": "application/vnd.google-apps.folder"
            }
            if parent_id:
                file_metadata["parents"] = [parent_id]
            folder_file = service.files().create(body=file_metadata, fields="id").execute()
            parent_id = folder_file.get("id")

    # Fișiere de urcat
    numar = json_data["numar"]
    base_name = f"{numar}_{client}"
    extensii = [".pdf", ".xlsx", ".json"]

    for ext in extensii:
        file_path = f"exports/{base_name}{ext}" if ext != ".json" else f"history/{base_name}{ext}"
        if not os.path.exists(file_path):
            continue
        media = MediaFileUpload(file_path, resumable=True)
        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [parent_id]
        }
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
