import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", page_icon="💼")

DATA_FILE = "dopyty.csv"

# Pôvodné testovacie dopyty pre opätovné načítanie
INITIAL_DATA = [
    {
        "ID": 1,
        "Datum_Vytvorenia": "2026-10-25 10:15",
        "Sluzba": "SI - Indiv. supervízia",
        "Hodiny": 4.0,
        "Miesto": "Jelka",
        "Krajina": "Slovensko (SR)",
        "Datum_Akcie": "2026-11-05",
        "Cas": "09:00",
        "Stav": "Nová",
        "Poznamka": "Individuálna supervízia - testovací dopyt Jelka"
    },
    {
        "ID": 2,
        "Datum_Vytvorenia": "2026-10-25 11:30",
        "Sluzba": "SK - Kolektívna supervízia",
        "Hodiny": 5.0,
        "Miesto": "Piešťany",
        "Krajina": "Slovensko (SR)",
        "Datum_Akcie": "2026-11-12",
        "Cas": "08:30",
        "Stav": "V riešení",
        "Poznamka": "Kolektívna supervízia pre charitný tím"
    },
    {
        "ID": 3,
        "Datum_Vytvorenia": "2026-10-25 14:00",
        "Sluzba": "Krízová intervencia",
        "Hodiny": 6.0,
        "Miesto": "Hodonín",
        "Krajina": "Česká republika (ČR)",
        "Datum_Akcie": "2026-11-18",
        "Cas": "10:00",
        "Stav": "Potvrdená",
        "Poznamka": "Akútna krízová intervencia a výjazd z Dúbravky"
    }
]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            df = pd.DataFrame(INITIAL_DATA)
            df.to_csv(DATA_FILE, index=False)
        return df
    else:
        df = pd.DataFrame(INITIAL_DATA)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if "dopyty" not in st.session_state:
    st.session_state.dopyty = load_data()

# Vlastné CSS pre prémiový dizajn a karty
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #2e3440; }
    .card { background-color: #1e222d; padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #00d4b1; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Asistent Štefana Šarközyho")

tabs = st.tabs(["📋 Dopyty", "➕ Nová požiadavka", "📊 Pipeline", "👥 Klienti", "⚙️ Nastavenia"])

# ZÁLOŽKA 1: DOPYTY
with tabs[0]:
    st.header("📋 Zoznam zaznamenaných dopytov")
    df = st.session_state.dopyty
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Celkom dopytov", len(df))
    col_m2.metric("Nové dopyty", len(df[df["Stav"] == "Nová"]))
    col_m3.metric("Potvrdené", len(df[df["Stav"] == "Potvrdená"]))
    
    st.divider()
    
    if df.empty:
        st.info("Zatiaľ neboli zaznamenané žiadne dopyty.")
    else:
        for idx, row in df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h4>#{row['ID']} - {row['Sluzba']} ({row['Miesto']}, {row['Krajina']})</h4>
                    <p><b>Termín:</b> {row['Datum_Akcie']} o {row['Cas']} | <b>Rozsah:</b> {row['Hodiny']} hod. | <b>Stav:</b> <span style="color:#00d4b1">{row['Stav']}</span></p>
                    <p><i>{row['Poznamka']}</i></p>
                </div>
                """, unsafe_allow_html=True)

        st.subheader("⚙️ Spracovanie a zmena stavu")
        selected_id = st.selectbox("Vyberte dopyt na úpravu (ID):", df["ID"].tolist())
        if selected_id:
            row = df[df["ID"] == selected_id].iloc[0]
            novy_stav = st.selectbox("Zmeniť stav dopytu:", ["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"], index=["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"].index(row['Stav']) if row['Stav'] in ["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"] else 0)
            if st.button("💾 Uložiť nový stav"):
                st.session_state.dopyty.loc[st.session_state.dopyty["ID"] == selected_id, "Stav"] = novy_stav
                save_data(st.session_state.dopyty)
                st.success("Stav dopytu bol aktualizovaný!")
                st.rerun()

# ZÁLOŽKA 2: NOVÁ POŽIADAVKA
with tabs[1]:
    st.header("1. Služby a bloky")
    sluzba = st.selectbox("Služba", ["SI - Indiv. supervízia", "SK - Kolektívna supervízia", "Krízová intervencia", "Koučing", "Vzdelávanie / Lektorovanie"])
    hodiny = st.number_input("Hodiny", min_value=1.0, max_value=12.0, value=4.0, step=0.5)

    st.header("2. Voľný termín a logistika (z Dúbravky)")
    col1, col2 = st.columns(2)
    with col1:
        krajina = st.radio("Krajina výjazdu", ["Slovensko (SR)", "Česká republika (ČR)"], horizontal=True)
    with col2:
        miesto = st.text_input("Miesto / Obec (voľný text pre SR aj ČR)", value="Jelka")

    col_d, col_t = st.columns(2)
    with col_d:
        datum_akcie = st.date_input("Dátum konania", datetime.now())
    with col_t:
        cas_akcie = st.time_input("Čas začiatku", datetime.now().time())

    poznamka = st.text_area("Poznámka / Špecifikácia dopytu", "")

    if st.button("💾 Uložiť dopyt do zoznamu", type="primary"):
        novy_id = int(st.session_state.dopyty["ID"].max() + 1) if not st.session_state.dopyty.empty else 1
        novy_riadok = {
            "ID": novy_id,
            "Datum_Vytvorenia": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Sluzba": sluzba,
            "Hodiny": hodiny,
            "Miesto": miesto,
            "Krajina": krajina,
            "Datum_Akcie": str(datum_akcie),
            "Cas": str(cas_akcie),
            "Stav": "Nová",
            "Poznamka": poznamka
        }
        st.session_state.dopyty = pd.concat([st.session_state.dopyty, pd.DataFrame([novy_riadok])], ignore_index=True)
        save_data(st.session_state.dopyty)
        st.success(f"Dopyt pre '{miesto}' bol uložený pod ID {novy_id}!")
        st.rerun()

# ZÁLOŽKA 3: PIPELINE
with tabs[2]:
    st.header("📊 Prehľad stavov (Pipeline)")
    if not st.session_state.dopyty.empty:
        st.bar_chart(st.session_state.dopyty["Stav"].value_counts())
    else:
        st.info("Žiadne dáta v pipeline.")
