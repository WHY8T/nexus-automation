# NEXUS — Personal Automation Engine

A local-first Python dashboard for safe file automation on Windows.

## Included
- File Organizer: preview and sort files into folders by extension.
- Duplicate Finder: detect identical files using SHA-256.
- Batch Renamer: preview and apply numbered filenames.
- Activity Logs: record completed organizer and renamer actions in SQLite.
- Custom NEXUS app icon (PNG) and editable SVG source.

## Run on Windows
1. Extract the ZIP.
2. Double-click `run_nexus.bat`.
3. Wait for dependencies to install.
4. Open the local Streamlit address shown in the terminal (usually http://localhost:8501).

For phone access on the same trusted Wi-Fi, use `run_nexus_lan.bat`, find your PC's IPv4 address with `ipconfig`, then open `http://YOUR-PC-IP:8501` on the phone. Keep the app on a trusted private network and do not expose port 8501 to the public internet.

## GitHub
See `GITHUB_SETUP.md` for commands to publish the source code.

## Safety and limitations
- Test on a copied folder first.
- The duplicate finder only reports files; it does not delete them.
- Organizer and renamer show a preview and require confirmation.
- Organizer skips destination filename collisions.
- This is currently a local Streamlit web app, not a standalone EXE or Android APK.
- A cloud-hosted copy runs on the cloud server; it cannot directly organize files on your PC or phone.
