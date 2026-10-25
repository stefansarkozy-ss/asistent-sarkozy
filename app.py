import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", page_icon="💼")

DATA_FILE = "dopyty.csv"

INITIAL_DATA = [
    {"ID": 1, "Datum_Vytvorenia": "2026-10-25 10:15", "Sluzba": "SI - Indiv. supervízia", "Hodiny": 4.0, "Miesto": "Jelka", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-05", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Stav": "Nová", "Poznamka": "Individuálna supervízia - testovací dopyt Jelka"},
    {"ID": 2, "Datum_Vytvorenia": "2026-10-25 11:30", "Sluzba": "SK - Kolektívna supervízia", "Hodiny": 5.0, "Miesto": "Piešťany", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-12", "Cas": "08:30", "Cestovny_Cas": 1.5, "Odchod": "07:00", "Stav": "Nová", "Poznamka": "Kolektívna supervízia pre charitný tím"},
    {"ID": 3, "Datum_Vytvorenia": "2026-10-25 14:00", "Sluzba": "Krízová intervencia", "Hodiny": 6.0, "Miesto": "Hodonín", "Krajina": "Česká republika (ČR)", "Datum_Akcie": "2026-11-18", "Cas": "10:00", "Cestovny_Cas": 2.0, "Odchod": "08:00", "Stav": "Nová", "Poznamka": "Akútna krízová intervencia a výjazd z Dúbravky"},
    {"ID": 4, "Datum_Vytvorenia": "2026-10-25 09:00", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "Cífer", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-02", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Stav": "Nová", "Poznamka": "p | Fakturácia: 240"},
    {"ID": 5, "Datum_Vytvorenia": "2026-10-25 09:15", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "CDR piešťany", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-04", "Cas": "10:00", "Cestovny_Cas": 1.5, "Odchod": "08:30", "Stav": "Nová", "Poznamka": "p | Fakturácia: 240"},
    {"ID": 6, "Datum_Vytvorenia": "2026-10-25 09:30", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "KC Príbeta", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-06", "Cas": "09:30", "Cestovny_Cas": 2.0, "Odchod": "07:30", "Stav": "V riešení", "Poznamka": "o | dohoda | Fakturácia: 240"},
    {"ID": 7, "Datum_Vytvorenia": "2026-10-25 09:45", "Sluzba": "supv", "Hodiny": 3.0, "Miesto": "KC Šaľa", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-08", "Cas": "10:00", "Cestovny_Cas": 1.0, "Odchod": "09:00", "Stav": "Potvrdená", "Poznamka": "p | Fakturácia: 180"},
    {"ID": 8, "Datum_Vytvorenia": "2026-10-25 10:00", "Sluzba": "supv", "Hodiny": 5.0, "Miesto": "dss javirinska", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-10", "Cas": "09:00", "Cestovny_Cas": 1.5, "Odchod": "07:30", "Stav": "Nová", "Poznamka": "p | Fakturácia: 300"},
    {"ID": 9, "Datum_Vytvorenia": "2026-10-25 10:15", "Sluzba": "supv", "Hodiny": 25.0, "Miesto": "pezinok Ospod", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-15", "Cas": "08:30", "Cestovny_Cas": 0.5, "Odchod": "08:00", "Stav": "Potvrdená", "Poznamka": "p | dohoda | Fakturácia: 1500"},
    {"ID": 10, "Datum_Vytvorenia": "2026-10-25 10:30", "Sluzba": "supv", "Hodiny": 6.0, "Miesto": "CDR pezinok", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-18", "Cas": "09:00", "Cestovny_Cas": 0.5, "Odchod": "08:30", "Stav": "Nová", "Poznamka": "p | Fakturácia: 360"},
    {"ID": 11, "Datum_Vytvorenia": "2026-10-25 11:00", "Sluzba": "supv", "Hodiny": 10.0, "Miesto": "Partizanske", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-22", "Cas": "09:00", "Cestovny_Cas": 2.0, "Odchod": "07:00", "Stav": "Potvrdená", "Poznamka": "p | Fakturácia: 600"}
]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if df.empty or 'ID' not in df.columns:
            df = pd.DataFrame(INITIAL_DATA)
            df.to_csv(DATA_FILE, index=False)
        if 'Cestovny_Cas' not in df.columns:
            df['Cestovny_Cas'] = 1.0
        if 'Odchod' not in df.columns:
            df['Odchod'] = "08:00"
        return df
    else:
        df = pd.DataFrame(INITIAL_DATA)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if "dopyty" not in st.session_state:
    st.session_state.dopyty = load_data()

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "📋 Dopyty"

if "edit_item" not in st.session_state:
    st.session_state.edit_item = None

st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 16px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #e0e0e0; border-left: 5px solid #ff4b4b; }
    .card-calendar { background-color: #f0f7f4; padding: 16px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #d0e8df; border-left: 5px solid #28a745; }
    .card h4 { margin-top: 0; color: #262730; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Asistent Štefana Šarközyho")

tabs_options = ["📋 Dopyty", "➕ Nová požiadavka", "📅 Kalendár", "📊 Pipeline", "👥 Klienti", "⚙️ Nastavenia"]
current_index = tabs_options.index(st.session_state.active_tab) if st.session_state.active_tab in tabs_options else 0

selected_tab = st.radio("Navigácia", tabs_options, index=current_index, horizontal=True, label_visibility="collapsed")
st.session_state.active_tab = selected_tab

st.divider()

if selected_tab == "📋 Dopyty":
    st.header("📋 Zoznam zaznamenaných dopytov")
    df = st.session_state.dopyty
    active_df = df[df["Stav"] != "Kalendár"]
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Celkom dopytov", len(active_df))
    col_m2.metric("Nové dopyty", len(active_df[active_df["Stav"] == "Nová"]))
    col_m3.metric("Potvrdené", len(active_df[active_df["Stav"] == "Potvrdená"]))
    
    st.divider()
    
    if active_df.empty:
        st.info("Zatiaľ neboli zaznamenané žiadne aktívne dopyty.")
    else:
        for idx, row in active_df.iterrows():
            c_info, c_btn = st.columns([4, 1])
            
            with c_info:
                st.markdown(f"""
                <div class="card">
                    <h4>#{row['ID']} - {row['Sluzba']} ({row['Miesto']}, {row['Krajina']})</h4>
                    <p><b>Termín:</b> {row['Datum_Akcie']} o {row['Cas']} | <b>Rozsah:</b> {row['Hodiny']} hod. | <b>Cesta:</b> {row.get('Cestovny_Cas', 1.0)} hod. (Odchod: {row.get('Odchod', '08:00')})</p>
                    <p><i>{row['Poznamka']}</i></p>
                </div>
                """, unsafe_allow_html=True)
            
            with c_btn:
                st.write("") 
                st.write("")
                if st.button("📅 Spracovať", key=f"btn_proc_{row['ID']}"):
                    st.session_state.edit_item = row.to_dict()
                    st.session_state.active_tab = "➕ Nová požiadavka"
                    st.rerun()

elif selected_tab == "➕ Nová požiadavka":
    item = st.session_state.edit_item
    if item:
        st.header(f"⚙️ Dokončenie a úprava dopytu #{item['ID']} ({item['Miesto']})")
        st.info("Upravte čas, logistiku a potvrďte pre presun do kalendára.")
    else:
        st.header("➕ Nová požiadavka")

    default_sluzba = item['Sluzba'] if item and 'Sluzba' in item else "supv"
    default_hodiny = float(item['Hodiny']) if item and 'Hodiny' in item else 4.0
    default_krajina = item['Krajina'] if item and 'Krajina' in item else "Slovensko (SR)"
    default_miesto = item['Miesto'] if item and 'Miesto' in item else ""
    default_cesta = float(item.get('Cestovny_Cas', 1.0)) if item else 1.0
    
    try:
        default_datum = datetime.strptime(str(item['Datum_Akcie']), "%Y-%m-%d").date() if item and pd.notna(item.get('Datum_Akcie')) else datetime.now().date()
    except:
        default_datum = datetime.now().date()

    try:
        default_cas = datetime.strptime(str(item['Cas']), "%H:%M").time() if item and pd.notna(item.get('Cas')) else datetime.now().time()
