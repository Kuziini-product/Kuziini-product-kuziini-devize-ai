@echo off
echo ================================
echo Sincronizare Git + protectie .env
echo ================================

git add .
git commit -m "Autosave before rebase" || echo [Info] Nicio modificare de salvat

git pull --rebase origin main

git push

if not exist ".env.example" (
    echo GITHUB_TOKEN=your_github_token_here> .env.example
    echo OPENAI_API_KEY=your_openai_api_key_here>> .env.example
    echo [Info] .env.example a fost creat
    git add .env.example
    git commit -m "Add .env.example from automation"
    git push
) else (
    echo [Info] .env.example exista deja
)

findstr /C:".env" .gitignore >nul 2>&1
if %errorlevel% neq 0 (
    echo .env>>.gitignore
    git add .gitignore
    git commit -m "Add .env to .gitignore from automation"
    git push
) else (
    echo [Info] .env este deja ignorat
)

echo ================================
echo Totul este sincronizat!
echo ================================
pause
