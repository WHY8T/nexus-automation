# Publish NEXUS to GitHub

Open PowerShell in the extracted NEXUS folder and run:

```powershell
git init
git add .
git commit -m "Initial NEXUS automation engine"
git branch -M main
git remote add origin https://github.com/WHY8T/nexus-automation.git
git push -u origin main
```

Before running these commands, create an empty repository named `nexus-automation`
under your GitHub account `WHY8T`. Do not initialize it with a README, license, or .gitignore.

Do not commit personal documents, downloads, passwords, `.venv`, or the local SQLite history.
The included `.gitignore` excludes the virtual environment and local history database.
