import streamlit as st
from pathlib import Path
from nexus.organizer import preview_organization, execute_organization
from nexus.duplicates import find_duplicates
from nexus.renamer import preview_rename, execute_rename
from nexus.database import init_db, add_log, get_logs

st.set_page_config(page_title="NEXUS | Automation Engine", page_icon="assets/nexus.png", layout="wide")
init_db()

st.markdown("""
<style>
.stApp { background: #0b1020; color: #e8eefc; }
[data-testid="stSidebar"] { background: #10182b; }
.block-container { padding-top: 2rem; max-width: 1400px; }
div[data-testid="stMetric"] { background: #131e34; border: 1px solid #243653; padding: 16px; border-radius: 14px; }
.stButton>button { border-radius: 10px; border: 1px solid #36527a; }
</style>
""", unsafe_allow_html=True)

brand_col, title_col = st.columns([1, 5], vertical_alignment="center")
with brand_col:
    st.image("assets/nexus-logo-trim.png", width=118)
with title_col:
    st.title("NEXUS")
    st.caption("PERSONAL AUTOMATION ENGINE  •  Local-first • Safe by design")

with st.sidebar:
    st.image("assets/nexus.png", width=64)
    st.markdown("## NEXUS")
    st.caption("PERSONAL AUTOMATION ENGINE")
    page = st.radio("WORKSPACE", ["Overview", "File Organizer", "Duplicate Finder", "Batch Renamer", "Activity Logs"])
    st.divider()
    st.caption("Your files stay on your computer. Nothing is uploaded.")

if page == "Overview":
    st.subheader("Command center")
    st.write("Automate repetitive file tasks with previews before changes are applied.")
    c1, c2, c3 = st.columns(3)
    logs = get_logs(1000)
    c1.metric("Recorded actions", len(logs))
    c2.metric("Available modules", "4")
    c3.metric("Execution mode", "Preview-first")
    st.info("Start with File Organizer to sort a test folder. We recommend trying it on a copy of your files first.")
    st.markdown("### Available modules")
    st.markdown("- **File Organizer** — sort files into folders by extension.\n- **Duplicate Finder** — identify identical files using SHA-256 hashes.\n- **Batch Renamer** — preview a consistent naming pattern before applying it.\n- **Activity Logs** — review actions performed by NEXUS.")

elif page == "File Organizer":
    st.subheader("File Organizer")
    folder = st.text_input("Folder to organize", placeholder=r"C:\Users\YourName\Downloads")
    if st.button("Scan and preview", type="primary"):
        if not folder or not Path(folder).is_dir():
            st.error("Enter an existing folder path.")
        else:
            items = preview_organization(Path(folder))
            st.session_state["organizer_preview"] = (folder, items)
    if "organizer_preview" in st.session_state:
        saved_folder, items = st.session_state["organizer_preview"]
        st.write(f"**Preview for:** `{saved_folder}`")
        if items:
            st.dataframe([{"File": str(src), "Destination": str(dst)} for src, dst in items], use_container_width=True)
            st.warning(f"{len(items)} file(s) will be moved. Existing destination names are skipped.")
            confirm = st.checkbox("I understand this will move files into extension folders.")
            if st.button("Execute organization", disabled=not confirm):
                moved, skipped = execute_organization(items)
                add_log("File Organizer", f"Moved {moved}; skipped {skipped}; folder {saved_folder}")
                st.success(f"Finished. Moved: {moved} • Skipped: {skipped}")
                del st.session_state["organizer_preview"]
        else:
            st.success("No files need organizing.")

elif page == "Duplicate Finder":
    st.subheader("Duplicate Finder")
    folder = st.text_input("Folder to scan", placeholder=r"C:\Users\YourName\Downloads", key="dupe_folder")
    if st.button("Find duplicates", type="primary"):
        if not folder or not Path(folder).is_dir():
            st.error("Enter an existing folder path.")
        else:
            with st.spinner("Hashing files..."):
                groups = find_duplicates(Path(folder))
            st.session_state["duplicates"] = (folder, groups)
    if "duplicates" in st.session_state:
        folder, groups = st.session_state["duplicates"]
        if not groups:
            st.success("No duplicate files found.")
        else:
            st.warning("These files have identical SHA-256 hashes. NEXUS will not delete anything.")
            for i, group in enumerate(groups, 1):
                with st.expander(f"Duplicate group {i} — {len(group)} files"):
                    for path in group:
                        st.code(str(path))
            st.metric("Duplicate groups", len(groups))

elif page == "Batch Renamer":
    st.subheader("Batch Renamer")
    folder = st.text_input("Folder containing files", placeholder=r"C:\Users\YourName\Pictures", key="rename_folder")
    prefix = st.text_input("New filename prefix", value="file")
    start = st.number_input("Starting number", min_value=0, value=1, step=1)
    if st.button("Preview rename", type="primary"):
        if not folder or not Path(folder).is_dir():
            st.error("Enter an existing folder path.")
        else:
            pairs, error = preview_rename(Path(folder), prefix, int(start))
            if error:
                st.error(error)
            else:
                st.session_state["rename_preview"] = (folder, pairs)
    if "rename_preview" in st.session_state:
        folder, pairs = st.session_state["rename_preview"]
        st.dataframe([{"Current name": a.name, "New name": b.name} for a, b in pairs], use_container_width=True)
        confirm = st.checkbox("I have checked the new filenames.")
        if st.button("Apply rename", disabled=not confirm):
            renamed, error = execute_rename(pairs)
            if error:
                st.error(error)
            else:
                add_log("Batch Renamer", f"Renamed {renamed} files in {folder}")
                st.success(f"Renamed {renamed} file(s).")
                del st.session_state["rename_preview"]

elif page == "Activity Logs":
    st.subheader("Activity Logs")
    logs = get_logs(500)
    if logs:
        st.dataframe([{"Time": t, "Module": m, "Details": d} for t, m, d in logs], use_container_width=True)
    else:
        st.info("No actions recorded yet.")
