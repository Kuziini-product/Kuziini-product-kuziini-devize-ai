
import os
import subprocess

def incarca_in_github(json_data):
    numar = json_data["numar"]
    client = json_data["client"]
    base_name = f"{numar}_{client}"

    mesaj = f"Deviz generat automat: {base_name}"

    try:
        subprocess.run(["git", "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", "."], check=True)
        subprocess.run(["git", "commit", "-m", mesaj], check=True)

        token = os.getenv("GH_TOKEN")
        repo_url = os.getenv("GH_REPO")

        if token and repo_url:
            repo_aut = repo_url.replace("https://", f"https://{token}@")
            subprocess.run(["git", "push", repo_aut], check=True)
        else:
            print("⚠️ Lipsesc variabilele GH_TOKEN sau GH_REPO")
    except subprocess.CalledProcessError as e:
        print("❌ Eroare Git:", e)
