
@echo off
set GH_TOKEN=GH_TOKENUL_TAU_AICI
set GH_REPO=https://github.com/utilizatorul-tau/nume-repo.git
cd /d %~dp0
call venv\Scripts\activate.bat
streamlit run streamlit_app.py
pause
