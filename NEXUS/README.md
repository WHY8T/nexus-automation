# NEXUS — Personal Automation Engine

A local-first Python dashboard for safe file automation on Windows.

## Included
- File Organizer: preview and sort files into folders by extension.
- Duplicate Finder: detect identical files using SHA-256.
- Batch Renamer: preview and apply numbered filenames.
- Activity Logs: record completed organizer and renamer actions in SQLite.
- Custom NEXUS octopus logo/icon (`assets/nexus.png`, `assets/nexus.ico`).

## Run on Windows
1. Open the `NEXUS` folder (the one that contains `app.py` and `run_nexus.bat`).
2. Double-click `run_nexus.bat` (in PowerShell: `.\run_nexus.bat` from inside that folder).
3. Wait for dependencies to install the first time.
4. Open http://localhost:8501 if the browser does not open by itself.

## Desktop icon (PC)
Double-click `create_desktop_shortcut.bat`. A **NEXUS** shortcut with the octopus icon appears on your Desktop.

## Phone (same Wi-Fi)
1. Run `run_nexus_lan.bat` on the PC and allow it through Windows Firewall (private network only).
2. Find the PC's IPv4 address with `ipconfig`.
3. On the phone open `http://YOUR-PC-IP:8501`.
4. Android Chrome: menu → **Add to Home screen**. iPhone Safari: Share → **Add to Home Screen**. The NEXUS icon is used.

Keep the app on a trusted private network and never expose port 8501 to the public internet.

## GitHub
See `GITHUB_SETUP.md`. To publish later changes:

```powershell
git add .
git commit -m "Describe your change"
git push
```

## Safety and limitations
- Test on a copied folder first.
- The duplicate finder only reports files; it does not delete them.
- Organizer and renamer show a preview and require confirmation.
- Organizer skips destination filename collisions.
- This is a local Streamlit web app, not a standalone EXE or Android APK.
- A cloud-hosted copy runs on the cloud server; it cannot directly organize files on your PC or phone.
