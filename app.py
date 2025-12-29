import streamlit as st
import json
import pathlib
import streamlit.components.v1 as components

st.set_page_config(page_title="Toolbox Hub", page_icon="🧰", layout="wide")
st.title("🧰 Toolbox Hub")

# Load apps catalog
catalog_path = pathlib.Path(__file__).parent / "apps_catalog.json"
if catalog_path.exists():
    with open(catalog_path, "r", encoding="utf-8") as f:
        apps = json.load(f)
else:
    apps = []

# Search input
query = st.text_input("Buscar (nombre, tags)", "")
cols = st.columns(3)

# Filter apps by query
filtered = []
for app in apps:
    blob = (app.get("name", "") + " " + " ".join(app.get("tags", []))).lower()
    if query.lower() in blob:
        filtered.append(app)

# "Modo mañana" button to open all apps
if st.button("🚀 Abrir todas las herramientas"):
    urls = [app["url"] for app in (filtered or apps)]
    components.html(
        f"""
        <script>
        const urls = {json.dumps(urls)};
        urls.forEach((u, i) => {{
            setTimeout(() => window.open(u, "_blank"), i * 250);
        }});
        </script>
        """,
        height=0,
    )

# Display app cards
for idx, app in enumerate(filtered):
    with cols[idx % 3]:
        st.subheader(app["name"])
        if app.get("tags"):
            st.caption(", ".join(app.get("tags", [])))
        st.write(app.get("desc", ""))
        st.page_link(app["url"], label="Abrir herramienta ↗", icon="🚀")
        st.page_link(app["repo"], label="Ver repo ↗", icon="🧑‍💻")
