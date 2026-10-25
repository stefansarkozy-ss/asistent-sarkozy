import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", page_icon="💼")

DATA_FILE = "dopyty.csv"

INITIAL_DATA = [
    {"ID": 1, "Datum_Vytvorenia": "2026-10-25 10:15", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "Cífer", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-02", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Cena_Sluzby": 220.0, "Cena_Cestovne": 45.0, "Km": 100, "Stav": "Nová", "Poznamka": "p | Fakturácia: 265"},
    {"ID": 2, "Datum_Vytvorenia": "2026-10-25 10:20", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "CDR piešťany", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-04", "Cas": "10:00", "Cestovny_Cas": 1.5, "Odchod": "08:30", "Cena_Sluzby": 220.0, "Cena_Cestovne": 85.0, "Km": 190, "Stav": "Nová", "Poznamka": "p | Fakturácia: 305"},
    {"ID": 3, "Datum_Vytvorenia": "2026-10-25 10:25", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "KC Príbeta", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-06", "Cas": "09:30", "Cestovny_Cas": 2.0, "Odchod": "07:30", "Cena_Sluzby": 220.0, "Cena_Cestovne": 120.0, "Km": 270, "Stav": "Nová", "Poznamka": "o | dohoda | Fakturácia: 340"},
    {"ID": 4, "Datum_Vytvorenia": "2026-10-25 10:30", "Sluzby": "SI - individuálna supervízia", "Hodiny": 3.0, "Miesto": "KC Šaľa", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-08", "Cas": "10:00", "Cestovny_Cas": 1.0, "Odchod": "09:00", "Cena_Sluzby": 165.0, "Cena_Cestovne": 65.0, "Km": 150, "Stav": "Nová", "Poznamka": "p | Fakturácia: 230"},
    {"ID": 5, "Datum_Vytvorenia": "2026-10-25 10:35", "Sluzby": "SI - individuálna supervízia", "Hodiny": 5.0, "Miesto": "dss javirinska", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-10", "Cas": "09:00", "Cestovny_Cas": 1.5, "Odchod": "07:30", "Cena_Sluzby": 275.0, "Cena_Cestovne": 20.0, "Km": 40, "Stav": "Nová", "Poznamka": "p | Fakturácia: 295"},
    {"ID": 6, "Datum_Vytvorenia": "2026-10-25 10:40", "Sluzby": "SI - individuálna supervízia", "Hodiny": 25.0, "Miesto": "pezinok Ospod", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-15", "Cas": "08:30", "Cestovny_Cas": 0.5, "Odchod": "08:00", "Cena_Sluzby": 1375.0, "Cena_Cestovne": 25.0, "Km": 50, "Stav": "Nová", "Poznamka": "p | dohoda | Fakturácia: 1400"},
    {"ID": 7, "Datum_Vytvorenia": "2026-10-25 10:45", "Sluzby": "SI - individuálna supervízia", "Hodiny": 6.0, "Miesto": "CDR pezinok", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-18", "Cas": "09:00", "Cestovny_Cas": 0.5, "Odchod": "08:30", "Cena_Sluzby": 330.0, "Cena_Cestovne": 25.0, "Km": 50, "Stav": "Nová", "Poznamka": "p | Fakturácia: 355"},
    {"ID": 8, "Datum_Vytvorenia": "2026-10-25 10:50", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "Kc Jelka", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-05", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Cena_Sluzby": 220.0, "Cena_Cestovne": 40.0, "Km": 90, "Stav": "Nová", "Poznamka": "Testovací dopyt Jelka"},
    {"ID": 9, "Datum_Vytvorenia": "2026-10-25 10:55", "Sluzby": "SI - individuálna supervízia", "Hodiny": 10.0, "Miesto": "Partizanske", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-22", "Cas": "09:00", "Cestovny_Cas": 2.0, "Odchod": "07:00", "Cena_Sluzby": 550.0, "Cena_Cestovne": 130.0, "Km": 290, "Stav": "Nová", "Poznamka": "p | Fakturácia: 680"}
]

HOURLY_RATES = {
    "SI - individuálna supervízia": 55.0,
    "SS - skupinová supervízia": 60.0,
    "KI - krízová intervencia": 60.0,
    "K - koučing": 60.0,
    "V - vzdelávanie": 60.0
}

# Zákonná amortizácia per km (2026 SR)
LEGAL_AMORTIZATION_PER_KM = 0.313 

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
        if 'Cena_Sluzby' not in df.columns:
            df['Cena_Sluzby'] = df.get('Cena_Fakturacia', 0.0)
        if 'Cena_Cestovne' not in df.columns:
            df['Cena_Cestovne'] = 0.0
        if 'Km' not in df.columns:
            df['Km'] = 0
        if 'Sluzby' not in df.columns and 'Sluzba' in df.columns:
            df['Sluzby'] = df['Sluzba']
        return df
    else:
        df = pd.DataFrame(INITIAL_DATA)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def sync_to_google_calendar_automatically(row):
    pass

if "dopyty" not in st.session_state:
    st.session_state.dopyty = load_data()

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dopyty"

if "edit_item" not in st.session_state:
    st.session_state.edit_item = None

if "service_blocks" not in st.session_state:
    st.session_state.service_blocks = [{"sluzba": "SI - individuálna supervízia", "hodiny": 4.0}]

st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 16px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #e0e0e0; border-left: 5px solid #ff4b4b; }
    .card-calendar { background-color: #f0f7f4; padding: 16px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #d0e8df; border-left: 5px solid #28a745; }
    .card h4 { margin-top: 0; color: #262730; }
    .calc-box { background-color: #eef7fc; padding: 15px; border-radius: 8px; border: 1px solid #bce0fd; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Asistent Štefana Šarközyho")

tabs_options = ["Dopyty", "Nová", "Pipeline", "Klienti", "AI Engine", "Export"]
current_index = tabs_options.index(st.session_state.active_tab) if st.session_state.active_tab in tabs_options else 0

selected_tab = st.radio("Navigácia", tabs_options, index=current_index, horizontal=True, label_visibility="collapsed")
st.session_state.active_tab = selected_tab

st.divider()

all_available_services = list(HOURLY_RATES.keys())

if selected_tab == "Dopyty":
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
            total_cena = round(float(row.get('Cena_Sluzby', 0.0)) + float(row.get('Cena_Cestovne', 0.0)), 2)
            with c_info:
                st.markdown(f"""
                <div class="card">
                    <h4>#{row['ID']} - {row['Sluzby']} ({row['Miesto']}, {row['Krajina']})</h4>
                    <p><b>Termín:</b> {row
